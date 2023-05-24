@echo off
REM Check Python version
py -3.11 -V >nul 2>&1
if errorlevel 1 (
  echo Python 3.11 is not installed. The program may not work as intended or at all. If you run into any errors, please delete the venv folder, install the correct version, and try again. Here's a link: https://www.python.org/downloads/release/python-3110/
  call python -m venv venv
  call venv\Scripts\activate.bat
  call pip install -r requirements.txt -q
  call python main.py
  pause
  exit /b
)

call py -3.11 -m venv venv
call venv\Scripts\activate.bat
call pip install -r requirements.txt -q
call python main.py
pause