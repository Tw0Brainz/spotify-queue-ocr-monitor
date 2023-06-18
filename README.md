Spotify Queue OCR Monitor
=========================

Spotify Queue OCR Monitor is a tool designed to integrate various functionalities including a chat box, a screen overlay, Optical Character Recognition (OCR), Spotify interaction, Open Sound Control (OSC) notifications, Avatar Parameter changes, and text-to-speech playback. The functionalities interact with each other according to user interactions or automatic processes.

Project Components
------------------

*   **ChatBox:** A GUI for chat interactions, log messages, and OCR capture area control.
*   **Overlay:** Provides a screen overlay. Color indication for OCR status.
*   **OcrThread:** Performs Optical Character Recognition on a screen area and sends potential song names matching the pattern "# song name" to the Spotify Thread.
*   **SpotifyQThread:** Handles Spotify interactions like song searching and queueing.
*   **OSCNotifier:** Sends Open Sound Control (OSC) notifications.
*   **AvatarParameterChanger:** Changes avatar parameters for a VRChat avatar using OSC.
*   **TTSPlayer:** Handles text-to-speech playback functionality.

Installation
------------

Clone the project from GitHub and execute the `setup.bat` script by double-clicking on it. The script will create a `.env` file, prompt you to enter your Spotify API credentials, and create a virtual environment where it installs the necessary Python packages.

If Python 3.11 is not installed on your machine, the script will warn you and create the virtual environment using your current Python version. If you run into any issues, please ensure Python 3.11 is installed and try running the script again.

You will also have the option to install PyTorch if you wish to use your GPU for OCR processing. It may be a good idea to edit the `setup.bat` script to change the `torch` package version to match your CUDA version. You can find the correct version [here](https://pytorch.org/get-started/locally/). Just edit the line:<br> 
<b><u>"call pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"</u></b><br>
 to use what's compatible with your system.

Usage
-----

Run the \`run.bat\` script. This will activate the virtual environment, install any updated requirements, and run the \`main.py\` file to start the application.

License
-------

This project is licensed under the MIT License.