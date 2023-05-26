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
        scale, height_scale, width_scale = 0.175, 0.75, 1
        self.chatbox = ChatBox()
        self.overlay = Overlay(scale=scale,height_scale=height_scale,width_scale=width_scale,border_thickness=3)  # Pass in necessary parameters
        self.ocr_thread = OcrThread(scale,height_scale,width_scale)  # Pass in necessary parameters
        self.spotify_thread = SpotifyQThread()
        self.osc_notifier = OSCNotifier()  # Pass in necessary parameters if not default
        self.tts_player = None  # Initialize to None, will be created with new TTS text

        # Connect signals and slots
        self.chatbox.new_message_signal.connect(self.handle_new_message)
        
        self.chatbox.new_message_signal.connect(self.osc_notifier.custom_message_signal)
        self.spotify_thread.song_added_to_queue.connect(self.osc_notifier.song_added_signal)
        self.spotify_thread.song_already_in_queue.connect(self.osc_notifier.song_already_in_queue_signal)
        
        self.ocr_thread.potential_song_found.connect(self.spotify_thread.song_search)

        # Start the OCR thread
        self.ocr_thread.start()
        self.osc_notifier.start()

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
