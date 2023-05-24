import pytesseract
import re

def process_image(screenshot):
    # set the path to the tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # apply OCR on the screenshot
    # --psm 6 is the page segmentation mode for a single uniform block of text
    text = pytesseract.image_to_string(screenshot,config="--psm 6").lower()
    text = ' '.join(text.split("\n"))

    # regex to match the format '@@ song name'
    pattern = r'@@(.*)'

    match = re.search(pattern, text)
    if match and "song name" not in match.group(1).strip():
        return match.group(1).strip()
    return None
