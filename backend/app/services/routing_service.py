import math
import requests
from typing import List, Tuple

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    p = math.pi / 180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 2 * r * math.asin(math.sqrt(a))

class RoutingService:
    def find_nearest_vehicle(self, vehicles: List[dict], target_lat: float, target_lng: float, required_type: str) -> dict:
        available = [v for v in vehicles if v['status'] == 'Available' and (required_type == 'Any' or v['vehicle_type'] == required_type)]
        if not available:
            return None
            
        # Check nearest actual distance
        nearest = available[0]
        min_dist = haversine_distance(target_lat, target_lng, nearest['lat'], nearest['lng'])
        
        for v in available[1:]:
            dist = haversine_distance(target_lat, target_lng, v['lat'], v['lng'])
            if dist < min_dist:
                min_dist = dist
                nearest = v
                
        # If the user is > 50km away (e.g. they are in India, but the mock vehicles are in New York)
        # We beautifully "teleport" the mock vehicle to be a local city branch 1-3km away so the demo works anywhere in the world!
        import random
        if min_dist > 50:
            nearest['lat'] = target_lat + random.uniform(-0.02, 0.02)
            nearest['lng'] = target_lng + random.uniform(-0.02, 0.02)
            
        return nearest

    def generate_route(self, start_lat: float, start_lng: float, end_lat: float, end_lng: float, skip_api: bool = False) -> Tuple[List[List[float]], int]:
        # Try fetching real streets from OSRM
        if not skip_api:
            try:
                url = f"http://router.project-osrm.org/route/v1/driving/{start_lng},{start_lat};{end_lng},{end_lat}?geometries=geojson"
                # Setting a higher timeout to prevent blocking if API is slow or throttling
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    if data.get('routes') and len(data['routes']) > 0:
                        coords = data['routes'][0]['geometry']['coordinates']
                        # OSRM returns [Lng, Lat], Leaflet expects [Lat, Lng]
                        route = [[lat, lng] for lng, lat in coords]
                        time_sec = int(data['routes'][0]['duration'])
                        return route, time_sec
            except Exception as e:
                print(f"OSRM Route Failed: {e}. Falling back to linear routing.")
            
        # Generating a straight line mock map route fallback
        route = [
            [start_lat, start_lng],
            [(start_lat + end_lat) / 2 + 0.001, (start_lng + end_lng) / 2 + 0.001],
            [end_lat, end_lng]
        ]
        
        dist_km = haversine_distance(start_lat, start_lng, end_lat, end_lng)
        time_seconds = int((dist_km / 40.0) * 3600)
        
        return route, time_seconds

routing_service = RoutingService()
