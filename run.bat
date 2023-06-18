@echo off
call venv\Scripts\activate.bat
call pip install -r requirements.txt -q
call python main.py
pause