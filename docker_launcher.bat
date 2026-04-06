@echo off
REM Docker Launcher for Hotel Mediterranee
title Hotel Mediterranee - Docker

cd /d "%~dp0"

echo.
echo ============================================
echo   Hotel Mediterranee - Docker Launcher
echo ============================================
echo.

:menu
cls
echo ============================================
echo   Choisissez une option:
echo ============================================
echo.
echo   1. Demarrer l'app (docker-compose up)
echo   2. Arreter l'app (docker-compose down)
echo   3. Redemarrer l'app
echo   4. Voir les logs en temps reel
echo   5. Construire l'image (rebuild)
echo   6. Ouvrir l'app dans le navigateur
echo   7. Quitter
echo.
echo ============================================
echo.

set /p choice="Votre choix (1-7): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto restart
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto build
if "%choice%"=="6" goto open
if "%choice%"=="7" goto exit

echo.
echo [ERROR] Choix invalide!
echo.
pause
goto menu

:start
echo.
echo [INFO] Demarrage de l'application...
docker-compose up -d
echo.
echo [SUCCESS] Application demarree!
echo          Acces: http://localhost:8501
echo.
timeout /t 3 /nobreak
start "" http://localhost:8501
pause
goto menu

:stop
echo.
echo [INFO] Arret de l'application...
docker-compose down
echo.
echo [SUCCESS] Application arretee!
echo.
pause
goto menu

:restart
echo.
echo [INFO] Redemarrage de l'application...
docker-compose down
docker-compose up -d
echo.
echo [SUCCESS] Application redemarree!
echo          Acces: http://localhost:8501
echo.
timeout /t 3 /nobreak
start "" http://localhost:8501
pause
goto menu

:logs
echo.
echo [INFO] Affichage des logs (Ctrl+C pour quitter)...
echo.
docker-compose logs -f
goto menu

:build
echo.
echo [INFO] Reconstruction de l'image Docker...
docker-compose up -d --build
echo.
echo [SUCCESS] Image reconstruite et application demarree!
echo.
pause
goto menu

:open
echo.
echo [INFO] Ouverture du navigateur...
start "" http://localhost:8501
echo.
pause
goto menu

:exit
echo.
echo [INFO] Fermeture...
echo.
exit /b 0
