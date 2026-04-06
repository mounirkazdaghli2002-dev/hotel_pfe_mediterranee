@echo off
REM Enhanced Launcher - Localhost (default) or Public with param
title Hotel App - Local/Offline Ready
cd /d "%~dp0"

echo [INFO] Dossier courant: %cd%
echo.

REM Kill existing first
echo [INFO] Arrêt des processus existants...
taskkill /F /IM streamlit.exe 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8501" ^| findstr "LISTENING" 2^>nul') do (
    taskkill /F /PID %%a 2>nul
)
timeout /t 1 /nobreak >nul

REM Activate venv if exists
if exist venv (
    echo [INFO] Activation venv...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] Pas de venv, utilisation Python systeme
)

REM Quick deps
echo [INFO] Installation des dependances...
pip install streamlit pandas python-dotenv PyYAML --upgrade

echo.
echo [INFO] Vérification app.py...
if not exist app.py (
    echo [ERROR] app.py non trouvé!
    pause
    exit /b 1
)

REM Check for public mode arg
if "%1"=="public" (
    echo [INFO] Mode PUBLIC activé
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr "192"') do set IP=%%a&set IP=%IP: =%
    echo [INFO] IP détectée: %IP%
    echo.
    echo ========================================
    echo Accès LOCAL: http://localhost:8501
    echo Accès PUBLIC: http://%IP%:8501
    echo ========================================
    echo.
    start "" http://localhost:8501
    start "" http://%IP%:8501
    echo [INFO] Démarrage Streamlit en mode PUBLIC...
    python -m streamlit run app.py --server.port=8501 --server.headless=true --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false
) else (
    echo [INFO] Mode LOCAL activé
    echo.
    echo ========================================
    echo Accès: http://localhost:8501
    echo ========================================
    echo.
    start "" http://localhost:8501
    echo [INFO] Démarrage Streamlit en mode LOCAL...
    python -m streamlit run app.py --server.port=8501 --server.headless=true --server.address=127.0.0.1
)

echo.
echo [INFO] Appuyez sur une touche pour terminer...
pause
