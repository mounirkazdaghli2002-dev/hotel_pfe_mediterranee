@echo off
REM Reliable Offline Launcher for Hotel App - No Internet Required
title Hotel Mediterranee - Offline Mode

cd /d "%~dp0"
echo Starting Hotel Mediterranee App (Offline Mode)...

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install Python 3.9+ from python.org
    timeout /t 10
    exit /b 1
)

REM Create/activate virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

REM Install minimal requirements (offline-friendly)
echo Installing dependencies...
pip install --upgrade pip
pip install streamlit pandas==2.3.3 python-dotenv

REM Init data if missing
if not exist chambres.csv (
    echo Initializing data files...
    python -c "
import pandas as pd
import os
# Create default rooms
rooms_data = []
for i in range(1, 75): rooms_data.append({'numero': str(1000+i), 'type': 'Standard', 'aile': 'A', 'statut': 'Libre', 'etage': 1})
pd.DataFrame(rooms_data).to_csv('chambres.csv', index=False)
print('chambres.csv created')
"
)
if not exist utilisateurs.json (
    python -c "
import json
users = {'admin': {'password': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'role': 'admin', 'nom': 'Admin'}}
with open('utilisateurs.json', 'w') as f: json.dump(users, f)
print('utilisateurs.json created')
"
)
if not exist maintenance_tasks.csv (
    pd.DataFrame(columns=['id', 'chambre', 'description', 'assigned_to', 'statut']).to_csv('maintenance_tasks.csv', index=False)
)

REM Run Streamlit headless (localhost only)
echo Starting app at http://localhost:8501
echo Press Ctrl+C to stop.
start "" http://localhost:8501
streamlit run app.py --server.port=8501 --server.headless=true --server.address=127.0.0.1 --server.enableCORS=false

pause

