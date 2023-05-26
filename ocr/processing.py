from mss import mss
from PIL import Image, ImageEnhance
from PyQt5.QtCore import QThread, pyqtSignal
import pytesseract
import re,os,sys,time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from util.utils import calculate_bounding_box

class OcrThread(QThread):
    potential_song_found = pyqtSignal(str)
    new_song_found = pyqtSignal(str)
    start_running = pyqtSignal()
    
    def __init__(self, SCALE, HEIGHT_SCALE, WIDTH_SCALE):
        super().__init__()
        
        left, top, box_width, box_height = calculate_bounding_box(SCALE, HEIGHT_SCALE, WIDTH_SCALE)
        
        self.left = left
        self.top = top
        self.box_width = box_width
        self.box_height = box_height
        
        self.last_input = None
        
    def capture_screen(self):
        # capture screenshot
        sct = mss()
        screenshot = sct.grab({'top':self.top,'left':self.left,'width':self.box_width,'height':self.box_height})
        self.pre_process_image(screenshot)
        
    
    def pre_process_image(self, screenshot):
        # Pre-process image for OCR
        image = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        # To B&W
        image = image.convert('1')
        self.extract_song_name(image)
        
        
    def extract_song_name(self, image):
        # set the path to the tesseract executable if needed
        # pytesseract.pytesseract.tesseract_cmd = r'path_to_your_tesseract_exe'
        
        # apply OCR on the screenshot
        # --psm 6 is the page segmentation mode for a single uniform block of text
        text = pytesseract.image_to_string(image,config="--psm 6")
        # normalize text
        text = text.lower()
        text = ' '.join(text.split("\n"))
    
        # regex to match the format '@@ song name'
        pattern = r'@@(.*)'
    
        match = re.search(pattern, text)
        
        if match:
            song_name = match.group(1).strip()
            if song_name != self.last_input and song_name:
                self.potential_song_found.emit(song_name)
                self.last_input = song_name
                self.new_song_found.emit(song_name)
                print(f'New song found: {song_name}')
    def run(self):
        while True:
            self.capture_screen()
            time.sleep(2.5)
                

if __name__=="__main__":
    qtThread = OcrThread(0.5, 1, 1)
    qtThread.start()
    qtThread.pre_process_image(r"D:\Users\btcbl\Documents\VSCode Projects\spotify-queue-ocr-monitor\util\OCR_Test.png")
    qtThread.wait()
    qtThread.quit()