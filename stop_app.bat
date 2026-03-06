@echo off
chcp 65001 >nul

echo.
echo ============================================
echo    Arreter Hotel Mediterranee
echo ============================================
echo.

:: Tuer le processus streamlit
taskkill /F /IM streamlit.exe 2>nul

:: Tuer tous les processus python qui utilisent le port 8501
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8501" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
)

echo.
echo ============================================
echo ✅ Application Hotel Mediterranee arretee!
echo ============================================
echo.

timeout /t 2 /nobreak >nul

:: Verifier que le serveur est bien arrete
netstat -ano | findstr ":8501" >nul
if %errorlevel%==0 (
    echo ⚠️ Le port 8501 est toujours utilise.
    echo    Veuillez verifier les processus dans le Gestionnaire des taches.
) else (
    echo Le serveur a ete arrete correctement.
)

echo.
pause

