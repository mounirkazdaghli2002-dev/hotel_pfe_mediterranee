@echo off
cd /d "%~dp0"
start "" http://localhost:8501
streamlit run app_simple.py --server.port=8501
pause

