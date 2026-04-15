from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any
import uuid
import json
import os
import random
from pydantic import BaseModel

from app.models import EmergencyInput, ClassificationResponse, DispatchResponse, DashboardData, Vehicle
from app.db import db
from app.services.ai_service import ai_service
from app.services.routing_service import routing_service
from app.services.big_data_service import big_data_service
import asyncio

app = FastAPI(title="Smart Emergency Response API - Native Mode")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static folder exists
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    await db.connect()
    ai_service.load_models()
    asyncio.create_task(big_data_service.generate_stream())

@app.on_event("shutdown")
async def shutdown_event():
    await db.close()
    big_data_service.stop_stream()

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("app/static/index.html", "r") as f:
        return f.read()

@app.post("/classify-emergency", response_model=ClassificationResponse)
async def classify_emergency(payload: EmergencyInput):
    category = ai_service.classify_text(payload.text)
    risk_score = ai_service.predict_risk(payload.lat, payload.lng, 10, 0.5)
    
    case_id = "MANUAL_" + str(uuid.uuid4())
    log_doc = {
        "_id": case_id,
        "case_id": case_id,
        "text": payload.text,
        "lat": payload.lat,
        "lng": payload.lng,
        "category": category,
        "risk_score": risk_score,
        "status": "Classified"
    }
    db.emergency_cases.append(log_doc)
    return ClassificationResponse(case_id=case_id, category=category, risk_score=risk_score)

@app.post("/dispatch", response_model=DispatchResponse)
async def dispatch_vehicle(case_id: str, lat: float, lng: float, category: str):
    req_type = 'Ambulance' if category == 'Medical' else 'Firetruck' if category == 'Fire' else 'Police Car' if category == 'Crime' else 'Any'
    
    nearest = routing_service.find_nearest_vehicle(db.vehicles, lat, lng, req_type)
    if not nearest:
        # Emergency fallback: Deploy whatever is available!
        nearest = routing_service.find_nearest_vehicle(db.vehicles, lat, lng, 'Any')
        if not nearest:
            raise HTTPException(status_code=404, detail="Critical: All city vehicles are currently deployed!")

    nearest['status'] = 'Dispatched'
    nearest['current_case_id'] = case_id
    
    route, time_sec = routing_service.generate_route(nearest['lat'], nearest['lng'], lat, lng)
    
    db.routing_logs.append({
        "case_id": case_id, "vehicle_id": nearest['id'], "route_geometry": route
    })
    
    for case in db.emergency_cases:
        if case["case_id"] == case_id:
            case["status"] = "Dispatched"
            case["vehicle_id"] = nearest["id"]
            case["route"] = route

    return DispatchResponse(
        case_id=case_id,
        assigned_vehicle_id=nearest['id'],
        estimated_time=time_sec,
        route_geometry=route
    )

@app.post("/resolve")
async def resolve_case(case_id: str):
    # Free up vehicle and resolve case
    for case in db.emergency_cases:
        if case["case_id"] == case_id:
            case["status"] = "Resolved"
            if "vehicle_id" in case:
                # Free the vehicle
                for v in db.vehicles:
                    if v["id"] == case["vehicle_id"]:
                        v["status"] = "Available"
                        v["current_case_id"] = None
    return {"message": "Case resolved"}

class LocationSync(BaseModel):
    lat: float
    lng: float

@app.post("/sync-location")
async def sync_location(req: LocationSync):
    db.city_center_lat = req.lat
    db.city_center_lng = req.lng
    
    # Teleport all currently available vehicles strictly to this new real-world city location precisely so they appear on screen!
    for v in db.vehicles:
        if v["status"] == "Available":
            v["lat"] = req.lat + random.uniform(-0.04, 0.04)
            v["lng"] = req.lng + random.uniform(-0.04, 0.04)
            
    return {"status": "synced", "lat": req.lat, "lng": req.lng}

@app.get("/dashboard-data", response_model=DashboardData)
async def get_dashboard_data():
    v_rows = db.vehicles
    vehicles = [Vehicle(**v) for v in v_rows]
    active_cases_list = [c for c in db.emergency_cases if c["status"] == "Dispatched" or c["status"] == "Classified"]
    active_cases = len(active_cases_list)
    
    # Merge recent classified cases and raw mock stream data to display
    recent_logs = []
    cases_top = [c for c in db.emergency_cases if c["status"] != "Resolved"][-5:]
    raw_top = db.raw_logs[:5]
    for c in list(reversed(cases_top)): recent_logs.append(c)
    for r in raw_top: recent_logs.append(r)
            
    return DashboardData(
        active_cases=active_cases,
        vehicles=vehicles,
        recent_logs=recent_logs[:10],
        active_cases_list=active_cases_list
    )
