from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication
from vrc.osc_notifier import OSCNotifier
from gui.overlay import Overlay, ChatBox, calculate_bounding_box
from multiprocessing import Process
from spotify.auth import authenticate
from spotify.api import search_song, check_song_in_queue, add_song_to_queue
from ocr.capture import capture_screen
from ocr.process import process_image
import sys, subprocess, time, os

SCALE, HEIGHT_SCALE, WIDTH_SCALE = 0.5,1.0,1.0

class TTSPlayer:
    def __init__(self, text):
        self.text = text
        self.venv_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
        self.edge_playback_location = os.path.join(self.venv_location, "Scripts", "edge-playback")
        self.command = [self.edge_playback_location, "-t", self.text]

    def play_text(self):
        # uses a separate process to play the text
        subprocess.Popen(self.command)

    def play_in_background(self):
        # create a new process for play_text function
        p = Process(target=self.play_text)
        p.start()

class MainApp(QObject):
    new_song_signal = pyqtSignal(str)

    def __init__(self, chat_box):
        super().__init__()
        self.sp = authenticate()
        self.osc_notifier = OSCNotifier()
        self.last_song = None
        self.chat_box = chat_box
        self.timer = QTimer()
        self.timer.timeout.connect(self.main_loop)
        self.timer.start(2500) # loop every 2.5 seconds

    def main_loop(self):
        left, top, box_width, box_height = calculate_bounding_box(SCALE, HEIGHT_SCALE, WIDTH_SCALE)
        screenshot = capture_screen(left, top, box_width, box_height)
        potential_song = process_image(screenshot)
        print(potential_song)

        if potential_song and potential_song != self.last_song:
            song_id, song_name = search_song(self.sp, potential_song)

            if song_id is not None:
                song_in_queue = check_song_in_queue(self.sp, song_id)

                if not song_in_queue:
                    add_song_to_queue(self.sp, song_id)
                    self.new_song_signal.emit(song_name)
        self.last_song = potential_song

        new_messages = self.chat_box.get_new_messages()
        for message in new_messages:
            tts = TTSPlayer(message)
            tts.play_in_background()
        self.chat_box.clear_messages()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    overlay = Overlay(SCALE, HEIGHT_SCALE, WIDTH_SCALE)
    chat_box = ChatBox()

    overlay.show()
    chat_box.show()

    main_app = MainApp(chat_box)
    main_app.new_song_signal.connect(main_app.osc_notifier.notify_song_added)

    sys.exit(app.exec_())
