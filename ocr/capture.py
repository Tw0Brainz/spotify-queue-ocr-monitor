import cv2
import pyautogui
import numpy as np

def capture_screen(sleft, stop, box_width, box_height):
    # capture screenshot
    screenshot = pyautogui.screenshot(region=(sleft, stop, box_width, box_height))
    
    # convert the image into numpy array representation
    screenshot = np.array(screenshot)

    # convert the BGR image into RGB image
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

    return screenshot
