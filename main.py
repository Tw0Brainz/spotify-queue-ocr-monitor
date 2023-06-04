from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot, QRect
from gui.overlay import Overlay
from gui.chatbox import ChatBox
from ocr.processing import OcrThread
from spotify.auth import SpotifyQThread
from vrc.osc_notifier import OSCNotifier, AvatarParameterChanger
from util.utils import TTSPlayer
import sys


class MainApplication(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        # Instantiate classes
        self.chatbox = ChatBox()
        self.chatbox.show()
        self.overlay = Overlay(self.chatbox.output_area, border_thickness=1)
        self.overlay.show()
        self.ocr_thread = OcrThread(self.chatbox.output_area)
        self.spotify_thread = SpotifyQThread()
        self.osc_notifier = OSCNotifier()
        self.avatar_changer = AvatarParameterChanger()
        self.tts_player = None

        # Connect signals and slots
        self.chatbox.new_message_signal.connect(self.handle_new_message) # type: ignore
        self.chatbox.capture_area_updated_signal.connect(self.update_capture_area) # type: ignore

        self.chatbox.new_message_signal.connect(self.osc_notifier.send_custom_message) # type: ignore
        self.spotify_thread.spotify_error.connect(self.chatbox.receive_error)
        self.spotify_thread.song_added_to_queue.connect(self.osc_notifier.song_added_signal)
        self.spotify_thread.song_added_to_queue.connect(self.avatar_changer.temporary_change_parameters)

        self.ocr_thread.potential_song_found.connect(self.spotify_thread.song_search)

        # Start the OCR thread
        self.ocr_thread.start()
        self.osc_notifier.start()

    @pyqtSlot(str)
    def handle_new_message(self, message: str):
        self.tts_player = TTSPlayer(message)
        self.tts_player.run()

    @pyqtSlot(QRect)
    def update_capture_area(self, new_capture_area: QRect):
        self.overlay.setGeometry(new_capture_area)
        self.ocr_thread.update_capture_area(new_capture_area)


if __name__ == '__main__':
    app = MainApplication()
    sys.exit(app.exec_())
