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
    ) else (
      echo .env file already exists and is not empty.
    )
  )
)

call python -m venv venv
call venv\Scripts\activate.bat
call pip install -r requirements.txt -q

pause