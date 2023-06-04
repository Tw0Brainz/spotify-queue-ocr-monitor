from PyQt5.QtCore import QThread, pyqtSignal, QRect, QMutexLocker, QMutex, QObject
from mss import mss
from PIL import Image, ImageEnhance
import easyocr
import re
import os
from mss.exception import ScreenShotError

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
        sct = mss()
        with QMutexLocker(self.locker):
            screenshot = sct.grab({
                'top': self.capture_area.top(),
                'left': self.capture_area.left(),
                'width': self.capture_area.width(),
                'height': self.capture_area.height()
            })
            self.pre_process_image(screenshot)

    def pre_process_image(self, screenshot):
        image = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        image.save('ocr/test.png')
        image = 'ocr/test.png'
        self.extract_song_name(image)

    def extract_song_name(self, image):
        text = self.reader.readtext(image, detail=0, paragraph=True, blocklist=',./;\'[]')
        print(text)
        os.remove(image)
        potential_matches = []
        if text:
            pattern = r'#(.*)'
            for text_line in text:
                match = re.search(pattern, text_line)
                if match:
                    potential_matches.append(match.group(1).lstrip('@'))
        else:
            match = None

        if potential_matches:
            for match in potential_matches:
                self.potential_song_found.emit(match)

    def run(self):
        while True:
            self.capture_screen()
            self.msleep(1500)
