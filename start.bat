@echo off
echo Starting Resume Screening System...

:: Navigate to the correct directory (where this batch file is)
cd /d "%~dp0"

:: Activate the virtual environment
call "../.venv/Scripts/activate.bat"

:: Run the application
python app.py

pause
