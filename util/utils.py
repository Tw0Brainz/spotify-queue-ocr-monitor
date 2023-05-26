from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QThread
import subprocess,os,sys



def calculate_bounding_box(scale:float =1, height_scale:float =1, width_scale:float =1):
    # Get the size of the screen
    screen_size = QDesktopWidget().screenGeometry(-1)

    # Calculate width and height based on scale
    width = screen_size.width() * scale * width_scale
    height = screen_size.height() * scale * height_scale

    # Calculate left and top coordinates for centering the overlay
    left = (screen_size.width() - width) // 2
    top = (screen_size.height() - height) // 2

    return [int(var) for var in [left, top, width, height]]

class TTSPlayer(QThread):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.venv_location = os.environ["VIRTUAL_ENV"]
        self.edge_playback_location = os.path.join(self.venv_location, "Scripts", "edge-playback")
        self.command = [self.edge_playback_location, "-t", self.text]

    def run(self):
        # uses a separate process to play the text
        subprocess.Popen(self.command)
        