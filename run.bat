@echo off
call python -m venv venv
call venv\Scripts\activate.bat
call pip install -r requirements.txt
call python main.py
pause