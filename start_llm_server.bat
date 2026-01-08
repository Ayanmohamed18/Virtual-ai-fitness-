@echo off
echo ========================================
echo ForeverFit AI - Starting LLM API Server
echo ========================================
echo.
echo Loading fine-tuned DeepSeek model...
echo This may take 2-3 minutes on first load.
echo.
echo Server will run on: http://localhost:8000
echo.
echo Keep this window open while using the app!
echo ========================================
echo.

cd /d "%~dp0"
call venv_py310\Scripts\activate.bat
python llm_api.py

pause
