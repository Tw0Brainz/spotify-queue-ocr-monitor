from PyQt5.QtCore import QThread, pyqtSignal, QRect, QMutexLocker, QMutex
from mss import mss
from PIL import Image, ImageEnhance
import pytesseract
import re
import time

class OcrThread(QThread):
    potential_song_found = pyqtSignal(str)

    def __init__(self, capture_area: QRect):
        super().__init__()
        self.locker = QMutex()
        self.capture_area = capture_area
        self.last_input = None

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
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1)
        image = image.convert('1')
        self.extract_song_name(image)

    def extract_song_name(self, image):
        text = pytesseract.image_to_string(image, config="--psm 6")
        text = text.lower()
        text = ' '.join(text.split("\n"))

        pattern = r'@@(.*)'
        match = re.search(pattern, text)

        if match:
            song_name = match.group(1).strip()
            if song_name != self.last_input and song_name:
                self.potential_song_found.emit(song_name)
                self.last_input = song_name
                print(f'New song found: {song_name}')
                time.sleep(1)

    def run(self):
        while not self.isInterruptionRequested():
            self.capture_screen()
