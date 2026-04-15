# AI-Powered Smart Emergency Response & Resource Optimization System

A robust, full-stack MVP simulating a smart city emergency responder system. It classifies incoming emergency messages using an NLP model, determines location risk, automatically allocates the nearest available vehicle, and calculates optimal routing to the appropriate hospital.

## Features

- **Emergency Classification**: AI model (TF-IDF + Random Forest) categorizes incoming unstructured logs (e.g., "my father is not breathing") into Medical, Fire, Crime, or Traffic Accident.
- **Resource Allocation**: Automates vehicle dispatching to the closest case location.
- **Route Optimization**: Uses Dijkstra's algorithm to calculate the shortest path between the emergency site, responding vehicle, and target hospital.
- **Real-Time Dashboard**: React SPA viewing live cases, vehicle status, and rendering maps using Leaflet.
- **Big Data Streaming Mock**: Simulates incoming streams of emergency events using FastAPI background tasks dropping raw data into MongoDB, alongside structured data maintained in PostgreSQL.

## Tech Stack

- **Frontend**: React, Vite, Leaflet, Vanila CSS (Aesthetic Glassmorphism UI)
- **Backend**: FastAPI, Python, Asyncpg, Motor
- **AI/ML**: Scikit-Learn, Pandas, NetworkX
- **Databases**: PostgreSQL (Relational schema for assets), MongoDB (NoSQL schema for high volume logging/streaming)
- **Deployment**: Docker, Docker Compose

## How to Run

1. Make sure you have Docker and Docker Compose installed.
2. In the root directory, run:
   ```bash
   docker-compose up --build
   ```
3. Access the dashboard: `http://localhost:5173`
4. Access the API documentation: `http://localhost:8000/docs`

## Data Pipeline Flow

1. Mock data generator (`synthetic_data_gen.py`) is run at build time.
2. Models are trained on start or build time (`train_classification_model.py`, `train_risk_model.py`).
3. Simulated logs are sent to the backend `/classify-emergency`.
4. Processed data and routes are saved to PostgreSQL. Raw logs stay in MongoDB.
5. The React frontend fetches state from `/dashboard-data` and renders.
