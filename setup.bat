@echo off

set "envFile=.env"

REM Check if the .env file exists
if exist "%envFile%" (
  echo .env file already exists.
) else (
  echo Creating .env file...
  echo Please enter your Spotify API credentials:

  :client_id_loop
  set /p client_id="Enter your Spotify client_id: "
  if "%client_id%"=="" (
      echo Client ID cannot be empty, please enter the value again.
      goto client_id_loop
  )

  :client_secret_loop
  set /p client_secret="Enter your Spotify client_secret: "
  if "%client_secret%"=="" (
      echo Client Secret cannot be empty, please enter the value again.
      goto client_secret_loop
  )

  set /p redirect_uri="Enter your Spotify redirect_uri (default: http://127.0.0.1:8194): "
  if "%redirect_uri%"=="" set redirect_uri=http://127.0.0.1:8194

  (
    echo SPOTIPY_CLIENT_ID="%client_id%"
    echo SPOTIPY_CLIENT_SECRET="%client_secret%"
    echo SPOTIPY_REDIRECT_URI="%redirect_uri%"
  ) > "%envFile%"

  echo .env file has been created or updated with your provided Spotify API credentials.
)

:venv_loop
REM Check Python version
py -3.11 -V >nul 2>&1
if errorlevel 1 (
  echo Python 3.11 is not installed. The program may not work as intended or at all. If you run into any errors, please delete the venv folder, install the correct version, and try again. Here's a link: https://www.python.org/downloads/release/python-3110/
  echo Creating virtual environment venv and installing dependencies...
  call python -m venv venv
  goto end
) else (
  echo Python 3.11 is installed.
  echo Creating virtual environment venv and installing dependencies...
  call py -3.11 -m venv venv
  goto end
  )

:end
call venv\Scripts\activate.bat

set /p InstallPyTorch=Do you want to install PyTorch to use your GPU for the OCR processing?? (Y/N): 
if /I "%InstallPyTorch%"=="Y" (
    call pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
)

call pip install -r requirements.txt
echo Setup complete.
pause
