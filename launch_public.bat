@echo off
REM Public LAN Access Launcher - Site accessible from other devices
title Hotel App - Public LAN Access
cd /d "%~dp0"

REM Kill existing Streamlit
call stop_app.bat

REM Install/upgrade deps quietly
pip install streamlit pandas python-dotenv --quiet --upgrade >nul 2>&1

REM Get local IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr "192"') do set IP=%%a
set IP=%IP: =%

echo.
echo Starting at http://localhost:8501
echo Also accessible at http://%IP%:8501 ^(LAN devices^)
echo Press Ctrl+C to stop, run stop_app.bat to kill.
echo.

start "" "http://localhost:8501"
start "" "http://%IP%:8501"

streamlit run app.py --server.port=8501 --server.headless=true --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false
pause

