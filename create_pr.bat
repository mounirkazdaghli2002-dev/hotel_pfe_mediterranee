@echo off
REM Script to stage, commit, push changes and create a pull request
REM Hotel Mediterranee - Streamlit Cloud Deployment Fix

cd /d C:\Users\LENOVO\hotel_pfe_mediterranee

echo ===== STAGING FILES =====
git add requirements.txt .streamlit/config.toml app.py push_github.bat

echo.
echo ===== COMMITTING CHANGES =====
git commit -m "Fix: Add requirements and Streamlit config for Cloud deployment

- Added requirements.txt with necessary dependencies
- Added .streamlit/config.toml for proper configuration
- Created push helper script
- Enables proper deployment to Streamlit Cloud"

echo.
echo ===== PUSHING TO GITHUB =====
git push -u origin blackboxai/feature/persistent-session-v2

echo.
echo ===== DONE =====
echo Changes pushed to: blackboxai/feature/persistent-session-v2
echo.
echo To create a Pull Request:
echo 1. Go to: https://github.com/mounirkazdaghli2002-dev/hotel_pfe_mediterranee
echo 2. Click "Compare & pull request"
echo 3. Set base: main, compare: blackboxai/feature/persistent-session-v2
echo 4. Click "Create pull request"
echo.
echo OR install GitHub CLI and run: gh pr create --base main --head blackboxai/feature/persistent-session-v2
pause
