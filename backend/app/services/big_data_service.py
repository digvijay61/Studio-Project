import asyncio
import random
import json
import os
from datetime import datetime
from app.db import db
from app.services.ai_service import ai_service
from app.services.routing_service import routing_service
import uuid

class BigDataService:
    def __init__(self):
        self.is_running = False

    async def generate_stream(self):
        self.is_running = True
        print("Started Autonomous City Simulation (Big Data Stream)")
        
        mock_events = [
            "Noise complaint nearby", "Minor traffic collision at intersection", "Fire alarm triggered in residential block",
            "Suspicious activity reported outside store", "Medical assistance requested - heart palpitations", "Tree fell on power line", "Dumpster fire in alleyway"
        ]

        while self.is_running:
            try:
                # 1. Generate autonomous event in the city dynamically bounded around user!
                lat = db.city_center_lat + random.uniform(-0.04, 0.04)
                lng = db.city_center_lng + random.uniform(-0.04, 0.04)
                text = random.choice(mock_events)
                
                # 2. Autonomous Classification
                category = ai_service.classify_text(text)
                risk_score = ai_service.predict_risk(lat, lng, 10, 0.5)
                
                case_id = str(uuid.uuid4())
                incident = {
                    "_id": case_id, "case_id": case_id, "text": text,
                    "lat": lat, "lng": lng, "category": category, "risk_score": risk_score, "status": "Classified"
                }
                
                # 3. Autonomous Dispatching
                req_type = 'Ambulance' if category == 'Medical' else 'Firetruck' if category == 'Fire' else 'Police Car' if category == 'Crime' else 'Any'
                nearest = routing_service.find_nearest_vehicle(db.vehicles, lat, lng, req_type)
                
                if nearest:
                    nearest['status'] = 'Dispatched'
                    nearest['current_case_id'] = case_id
                    route, time_sec = routing_service.generate_route(nearest['lat'], nearest['lng'], lat, lng, skip_api=True)
                    incident["status"] = "Dispatched"
                    incident["vehicle_id"] = nearest["id"]
                    incident["route"] = route
                    db.routing_logs.append({"case_id": case_id, "vehicle_id": nearest['id'], "route_geometry": route})
                    
                db.emergency_cases.append(incident)
                
                # Keep memory clean
                if len(db.emergency_cases) > 50:
                    resolved_idx = next((i for i, c in enumerate(db.emergency_cases) if c['status'] == 'Resolved'), None)
                    if resolved_idx is not None:
                        db.emergency_cases.pop(resolved_idx)
                    else:
                        db.emergency_cases.pop(0)
                        
            except Exception as e:
                pass
            
            # Generate a new event every 15 seconds automatically
            await asyncio.sleep(15)

    def stop_stream(self):
        self.is_running = False

big_data_service = BigDataService()
