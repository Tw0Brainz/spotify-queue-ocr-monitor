from mss import mss
from PIL import Image, ImageFilter, ImageEnhance

def capture_screen(left, top, box_width, box_height):
    
    sct = mss()
    # capture screenshot
    screenshot = sct.grab({'top':top,'left':left,'width':box_width,'height':box_height})
    
    # Pre-process image for OCR
    image = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    
    # To B&W
    image = image.convert('1')
    image = image.filter(ImageFilter.MedianFilter())


    return image
