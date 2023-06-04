from PyQt5.QtCore import QThread, pyqtSignal, QRect, QMutexLocker, QMutex
from mss import mss
import easyocr
import re
import numpy as np

class OcrThread(QThread):
    potential_song_found = pyqtSignal(str)

    def __init__(self, capture_area: QRect):
        super().__init__()
        self.locker = QMutex()
        self.capture_area = capture_area
        self.last_input = None
        self.reader = easyocr.Reader(['en'], gpu=True)

    def update_capture_area(self, new_capture_area: QRect):
        with QMutexLocker(self.locker):
            self.capture_area = new_capture_area

    def capture_screen(self):
        with mss() as sct:
            with QMutexLocker(self.locker):
                screenshot = sct.grab({
                    'top': self.capture_area.top(),
                    'left': self.capture_area.left(),
                    'width': self.capture_area.width(),
                    'height': self.capture_area.height()
                })
        self.pre_process_image(screenshot)

    def pre_process_image(self, screenshot):
        image = np.array(screenshot, dtype=np.uint8)
        self.extract_song_name(image)

    def extract_song_name(self, image):
        text = self.reader.readtext(image, detail=0, paragraph=True, blocklist=',./;\'[]|')
        print(text)
        potential_matches = []
        if text:
            pattern = r'#(.*)'
            for text_line in text:
                match = re.search(pattern, text_line) # type: ignore
                if match:
                    potential_matches.append(match.group(1))
        else:
            match = None

        if potential_matches:
            for match in potential_matches:
                self.potential_song_found.emit(match)

    def run(self):
        while True:
            self.capture_screen()
            self.msleep(1500)
