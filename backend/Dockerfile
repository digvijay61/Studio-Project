FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for compilation of some packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-generate synthetic data and models during build so the app starts fast
COPY ../ml /ml
RUN python /ml/synthetic_data_gen.py
RUN python /ml/train_classification_model.py
RUN python /ml/train_risk_model.py

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
