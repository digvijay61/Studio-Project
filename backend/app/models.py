from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any

class EmergencyInput(BaseModel):
    text: str
    lat: float
    lng: float

class ClassificationResponse(BaseModel):
    case_id: str
    category: str
    risk_score: float

class Vehicle(BaseModel):
    id: int
    vehicle_type: str
    status: str
    lat: float
    lng: float
    current_case_id: Optional[str] = None

class DispatchResponse(BaseModel):
    case_id: str
    assigned_vehicle_id: int
    estimated_time: int
    route_geometry: Any

class DashboardData(BaseModel):
    active_cases: int
    vehicles: List[Vehicle]
    recent_logs: List[dict]
    active_cases_list: List[dict]
