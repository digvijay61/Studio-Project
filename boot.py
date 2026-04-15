import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

def run_cmd(cmd, cwd=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== Bootstrapping Smart Emergency System ===")
    
    # 1. Install Dependencies
    print("\n--- Installing pure-python dependencies ---")
    run_cmd(f"{sys.executable} -m pip install -r backend/requirements.txt")
    
    # 2. Generate Synthetic Data
    print("\n--- Generating ML Data ---")
    run_cmd(f"{sys.executable} ml/synthetic_data_gen.py", cwd=BASE_DIR)
    
    # 3. Train Models
    print("\n--- Training AI Models ---")
    run_cmd(f"{sys.executable} ml/train_classification_model.py", cwd=BASE_DIR)
    run_cmd(f"{sys.executable} ml/train_risk_model.py", cwd=BASE_DIR)
    
    # 4. Start Server
    print("\n--- Starting FastAPI Backend & UI ---")
    # Using python -m uvicorn instead of uvicorn directly to avoid PATH issues on Windows
    run_cmd(f"{sys.executable} -m uvicorn app.main:app --host 127.0.0.1 --port 8000", cwd=BASE_DIR / "backend")
