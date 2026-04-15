import json
import os
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "emergency_logs.json"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

def train_classification_model():
    if not DATA_PATH.exists():
        print("Data not found, please run synthetic_data_gen.py first.")
        return

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    X = [item["text"] for item in data]
    y = [item["label"] for item in data]

    # Create a pipeline with TF-IDF and ExtraTrees for maximum precision
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=10000, ngram_range=(1, 2))),
        ('clf', ExtraTreesClassifier(n_estimators=500, random_state=42, n_jobs=-1))
    ])

    pipeline.fit(X, y)
    
    model_path = MODELS_DIR / "classification_model.joblib"
    joblib.dump(pipeline, model_path)
    print(f"Classification model trained and saved to {model_path}")

if __name__ == "__main__":
    train_classification_model()
