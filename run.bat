@echo off

set "envFile=.env"

REM Check if the .env file exists
if not exist %envFile% (
  (
    echo SPOTIPY_CLIENT_ID=""
    echo SPOTIPY_CLIENT_SECRET=""
    echo SPOTIPY_REDIRECT_URI=""
  ) > %envFile%
  echo Empty .env file created with required empty values for Spotify API.
  echo Please fill out the .env file and run the run.bat file again.
  pause
  exit /b
) else (
  REM Check if the .env file is empty
  for %%I in (%envFile%) do (
    if %%~zI equ 0 (
      (
        echo SPOTIPY_CLIENT_ID=""
        echo SPOTIPY_CLIENT_SECRET=""
        echo SPOTIPY_REDIRECT_URI=""
      ) > %envFile%
      echo .env file was empty. Required empty values for Spotify API added.
      echo Please fill out the .env file and run the run.bat file again.
      pause
      exit /b
    ) else (
      echo .env file already exists and is not empty.
    )
  )
)

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
