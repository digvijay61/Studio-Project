import joblib
import os
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ml" / "models"
CLASSIFICATION_MODEL_PATH = BASE_DIR / "classification_model.joblib"
RISK_MODEL_PATH = BASE_DIR / "risk_model.joblib"

class AIService:
    def __init__(self):
        self.clf_model = None
        self.risk_model = None

    def load_models(self):
        try:
            self.clf_model = joblib.load(CLASSIFICATION_MODEL_PATH)
            self.risk_model = joblib.load(RISK_MODEL_PATH)
            print("Models loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}. Ensure they are generated.")

    def classify_text(self, text: str) -> str:
        if not self.clf_model:
            return "Unknown"
        prediction = self.clf_model.predict([text])
        return prediction[0]

    def predict_risk(self, lat: float, lng: float, past_incidents: int, traffic_density: float) -> float:
        if not self.risk_model:
            return 50.0
        df = pd.DataFrame([{
            'lat': lat,
            'lng': lng,
            'past_incidents': past_incidents,
            'traffic_density': traffic_density
        }])
        score = self.risk_model.predict(df)[0]
        return float(score)

ai_service = AIService()
