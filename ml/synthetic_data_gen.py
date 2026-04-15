import json
import os
import random
from pathlib import Path

# Create data dir
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def generate_emergency_texts():
    cases = [
        ("My father is having a heart attack, he's not breathing!", "Medical"),
        ("There is a massive fire in the building next door!", "Fire"),
        ("Someone just robbed the convenience store with a gun.", "Crime"),
        ("Two cars just crashed on the highway intersection, looks bad.", "Traffic"),
        ("I need an ambulance, my wife is going into labor.", "Medical"),
        ("The kitchen caught on fire, smoke is everywhere.", "Fire"),
        ("There's a suspicious person looking into houses.", "Crime"),
        ("Major pileup on Route 9, multiple cars involved.", "Traffic"),
        ("Send help, someone collapsed on the street.", "Medical"),
        ("A dumpster is on fire in the alley.", "Fire"),
        ("I just saw a hit and run.", "Traffic"),
        ("My house was broken into while I was away.", "Crime")
    ]
    # Augment cases for more variance
    dataset = []
    for _ in range(100):
        text, label = random.choice(cases)
        dataset.append({"text": text, "label": label})
    
    with open(DATA_DIR / "emergency_logs.json", "w") as f:
        json.dump(dataset, f, indent=2)

def generate_historical_risk_data():
    # Historical data to predict zone risk (lat, lng, past_incidents, traffic_density)
    data = []
    for _ in range(200):
        lat = random.uniform(40.7000, 40.8000)
        lng = random.uniform(-74.0500, -73.9000)
        past_incidents = random.randint(0, 100)
        traffic_density = random.uniform(0.1, 1.0)
        
        # Simple rule to construct "risk_score" (0 to 100)
        risk_score = min(100, int((past_incidents * 0.5) + (traffic_density * 50) + random.randint(-10, 10)))
        risk_score = max(0, risk_score)
        
        data.append({
            "lat": lat,
            "lng": lng,
            "past_incidents": past_incidents,
            "traffic_density": traffic_density,
            "risk_score": risk_score
        })
    
    with open(DATA_DIR / "risk_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    generate_emergency_texts()
    generate_historical_risk_data()
    print("Synthetic data generated in ml/data/")
