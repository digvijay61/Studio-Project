import os
import json

class Database:
    def __init__(self):
        self.city_center_lat = 40.7000
        self.city_center_lng = -74.0500
        self.vehicles = [
            {"id": 1, "vehicle_type": "Ambulance", "status": "Available", "lat": 40.7300, "lng": -73.9950},
            {"id": 2, "vehicle_type": "Ambulance", "status": "Available", "lat": 40.7400, "lng": -73.9800},
            {"id": 3, "vehicle_type": "Firetruck", "status": "Available", "lat": 40.7100, "lng": -74.0100},
            {"id": 4, "vehicle_type": "Police Car", "status": "Available", "lat": 40.7500, "lng": -73.9900},
            {"id": 5, "vehicle_type": "Ambulance", "status": "Maintenance", "lat": 40.7800, "lng": -73.9700}
        ]
        self.emergency_cases = []
        self.raw_logs = []
        self.routing_logs = []

    async def connect(self):
        print("Mock DB in-memory structures initialized.")

    async def close(self):
        pass

db = Database()
