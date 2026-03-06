@echo off
chcp 65001 >nul
title Hotel Mediterranee - Internet

echo.
echo ============================================
echo    Hotel Mediterranee - Acces Internet
echo ============================================
echo.
echo Lancement de l'application avec Cloudflare Tunnel...
echo.
echo Vous recevrez une URL comme:
echo   https://votre-nom.trycloudflare.com
echo.
echo Attention: Cette URL change a chaque demarrage!
echo.

cd /d "%~dp0"

echo Lancement de Streamlit...
start "" python -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true

echo.
echo Attente du demarrage de Streamlit (10 secondes)...
timeout /t 10 /nobreak > nul

echo Lancement du tunnel Cloudflare...
start "" cloudflared.exe tunnel --url http://localhost:8501

echo.
echo ============================================
echo    Instructions:
echo ============================================
echo.
echo 1. Attendez quelques secondes
echo 2. Regardez l'URL dans la fenetre qui apparait
echo 3. Utilisez cette URL pour acceder depuis
echo    n'importe quel appareil (meme 4G)
echo.
echo Pour arreter: fermez les fenetres Streamlit
echo.
echo ============================================
echo.

pause

