@echo off
echo Starting ForeverFit LLM API Server...
echo Host: 0.0.0.0 (Accessible on LAN)
echo Port: 8000
echo.
echo NOTE: Ensure your firewall allows inbound traffic on port 8000.
echo.

call .\venv_py310\Scripts\activate.bat
python llm_api.py
pause
