import json
import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "risk_data.json"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

def train_risk_model():
    if not DATA_PATH.exists():
        print("Data not found, please run synthetic_data_gen.py first.")
        return

    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    X = df[['lat', 'lng', 'past_incidents', 'traffic_density']]
    y = df['risk_score']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Risk model trained. MSE: {mse:.2f}")

    model_path = MODELS_DIR / "risk_model.joblib"
    joblib.dump(model, model_path)
    print(f"Risk model saved to {model_path}")

if __name__ == "__main__":
    train_risk_model()
