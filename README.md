# Spotify Queue OCR Monitor

Spotify Queue OCR Monitor is a Python project that uses optical
character recognition (OCR) to monitor a designated area of your screen
for song names in an in-game chat format. When a song name is detected,
the program automatically searches for the song on Spotify and adds it
to your queue if it\'s not already there.

This project combines the power of OpenCV for screen capturing,
Tesseract OCR for optical character recognition, and Spotipy to interact
with the Spotify Web API.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

-   Written on [Python version 3.11.0](https://www.python.org/downloads/release/python-3110/)\
    and [pip version 22.3](https://pypi.org/project/pip/).
-   Spotify account
-   Registered Spotify App to obtain your `client_id`, `client_secret`,
    and `redirect_uri`. You can register a new App on the [Spotify
    Developer Dashboard](https://developer.spotify.com/dashboard/)

### Installing Spotify Queue OCR Monitor

To install Spotify Queue OCR Monitor, follow these steps:

1.  Clone the repo:\
    `git clone https://github.com/tw0brainz/spotify-queue-ocr-monitor.git`
2.  Navigate to the project directory:\
    `cd spotify-queue-ocr-monitor`
3.  Create the virtual environment, create the `.env` template file, install dependencies by executing the following:\
    `./setup.bat`

### Setting Up Spotify API Credentials

Open the newly created file named `.env` in the root directory of the project and
add the following environment variables with your Spotify credentials:


    SPOTIPY_CLIENT_ID=<your-spotify-client-id>
    SPOTIPY_CLIENT_SECRET=<your-spotify-client-secret>
    SPOTIPY_REDIRECT_URI=<your-spotify-redirect-uri>

### Setting Up Tesseract OCR

This project uses Tesseract OCR(Version 5.3.1) via pytesseract. Please ensure that
[Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) is correctly installed on your system and pytesseract is
correctly configured. If Tesseract OCR is installed at a non-standard
location, make sure to update the `tesseract_cmd` variable in
`ocr/process.py`:


    pytesseract.pytesseract.tesseract_cmd = r'path_to_your_tesseract_exe'

Replace `'path_to_your_tesseract_exe'` with the path to your Tesseract
OCR executable.

## Usage

To run Spotify Queue OCR Monitor, execute:\
`./run.bat`

By default, the program scans the center of the screen every 3 seconds.
The bounding box parameters and the capture rate can be adjusted in the
`main.py` file.

### GUI Overlay

The program creates a green overlay on your screen to indicate the area
that is being monitored. This is accomplished with a Tkinter window
defined in `gui/overlay.py`.

### Spotify API Calls

The Spotipy library is used to make Spotify API calls to search for
songs, verify if they are already in your queue, and add them to your
queue if they are not. These actions are defined in `spotify/api.py`.

### OCR Processing

The program uses OpenCV and Tesseract OCR via pytesseract to capture
screenshots and extract text from them. The image capture and processing
functionalities are defined in the `ocr` module.

### VRC OSC Chatbox Notifications

The program uses Python-OSC to send chatbox messages providing status updates as well as how to request a song. The default parameters for the vrc_osc_notifier should work for most but you can pass in a string IP(default:"127.0.0.1" and integer Port number(default:9000) if you've changed your vrc launch options for the OSC server 

## Running Tests

You can run tests to validate the OCR and Spotify functionalities
using:\
`./tests.bat`

## Contributing to Spotify Queue OCR Monitor

To contribute to Spotify Queue OCR Monitor, follow these steps:

1.  Fork the repository.
2.  Create a new branch: `git checkout -b '<branch_name>'`.
3.  Make your changes and commit them:
    `git commit -m '<commit_message>'`.
4.  Push to the original branch:
    `git push origin '<project_name>/<location>'`.
5.  Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull
request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
