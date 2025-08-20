@echo off
cd /d "%~dp0"

:: Activate virtual environment
call "../.venv/Scripts/activate.bat"

:: Set Python path
set PYTHONPATH=%PYTHONPATH%;src

:: Run the web interface
python src/web_interface.py
