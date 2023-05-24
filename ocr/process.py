import pytesseract
import re

def process_image(screenshot):
    # set the path to the tesseract executable
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # apply OCR on the screenshot
    text = pytesseract.image_to_string(screenshot).lower()

    # regex to match the format 'djreq: song name'
    pattern = r'djreq: (.*)'

    match = re.search(pattern, text)
    if match:
        return match.group(1)

    return None
