from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
import subprocess,os

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
        
if __name__ == "__main__":
    app = QApplication([])
    player = TTSPlayer("Hello world")
    player.run()