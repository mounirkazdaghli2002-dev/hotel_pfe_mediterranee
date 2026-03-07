@echo off
chcp 65001 >nul
title Hotel Mediterranee

echo.
echo ============================================
echo    Hotel Mediterranee - Lancement
echo ============================================
echo.
echo Lancement de l'application en arriere-plan...
echo.

cd /d "%~dp0"

:: Verifier si le port 8501 est deja utilise
netstat -ano | findstr ":8501" >nul
if %errorlevel%==0 (
    echo Le serveur semble deja demarre!
    echo Accedez a: http://localhost:8501
    echo.
    pause
    exit /b 0
)

:: Lancer Streamlit en arriere-plan avec PowerShell (sans fenetre)
powershell -Command "Start-Process -FilePath 'python' -ArgumentList '-m','streamlit','run','app.py','--server.port=8501','--server.headless=true','--browser.gatherUsageStats=false' -WindowStyle Hidden"

echo Demarrage en cours...
echo.

:: Attendre que le serveur soit pret
set attempts=0
:wait_loop
timeout /t 2 /nobreak >nul 2>&1
set /a attempts+=1

curl -s -o nul -w "%%{http_code}" http://localhost:8501 > tmp.txt 2>nul
set /p code=<tmp.txt
del tmp.txt 2>nul

if "%code%"=="200" goto :server_ready
if %attempts% LSS 10 goto :wait_loop

:server_ready
if "%code%"=="200" (
    echo.
    echo ============================================
    echo ✅ Succes! L'application est accessible!
    echo ============================================
    echo.
    echo    Adresse: http://localhost:8501
    echo.
    echo Pour fermer l'application:
    echo    Double-cliquez sur stop_app.bat
    echo.
) else (
    echo.
    echo ⚠️ Le serveur est en cours de demarrage.
    echo    Veuillez patienter et essayer d'acceder a:
    echo    http://localhost:8501
    echo.
)

echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul

