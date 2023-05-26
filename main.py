from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot
from gui.overlay import Overlay,ChatBox
from ocr.processing import OcrThread
from spotify.auth import SpotifyQThread
from vrc.osc_notifier import OSCNotifier
from util.utils import TTSPlayer
import sys
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Instantiate your classes
        self.chatbox = ChatBox()
        self.overlay = Overlay(scale=0.5,height_scale=1,width_scale=1,border_thickness=3)  # Pass in necessary parameters
        self.ocr_thread = OcrThread(0.5,1,1)  # Pass in necessary parameters
        self.spotify_thread = SpotifyQThread()
        self.osc_notifier = OSCNotifier()  # Pass in necessary parameters if not default
        self.tts_player = None  # Initialize to None, will be created with new TTS text

        # Connect signals and slots
        self.chatbox.new_message_signal.connect(self.handle_new_message)
        self.ocr_thread.potential_song_found.connect(self.spotify_thread.song_search)
        self.spotify_thread.song_added_to_queue.connect(self.osc_notifier.notify_song_added)

        # Start the OCR thread
        self.ocr_thread.start()

        # Set the chatbox as the central widget
        self.setCentralWidget(self.chatbox)

    @pyqtSlot(str)
    def handle_new_message(self, message: str):
        self.tts_player = TTSPlayer(message)
        self.tts_player.run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
