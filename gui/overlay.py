from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel, QDesktopWidget, QApplication
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import screeninfo

# def calculate_bounding_box(scale: float=1, height_scale: float=1,width_scale: float=1):
#     """Calculate the parameters of a bounding box at the center of the main monitor.

#     Args:
#         scale (float): Scaling factor for the size of the bounding box
#         height_scale (float): Scaling factor for the size of the height
#         width_scale (float): Scaling factor for the size of the width

#     Returns:
#         left (int): The horizontal coordinate of the top-left corner of the bounding box
#         top (int): The vertical coordinate of the top-left corner of the bounding box
#         box_width (int): The width of the bounding box
#         box_height (int): The height of the bounding box
#     """
#     monitor = screeninfo.get_monitors()[0]
#     box_width = int(round(monitor.width * scale * width_scale))
#     box_height = int(round(monitor.height * scale * height_scale))
#     left = int(round((monitor.width - box_width) // 2))
#     top = int(round((monitor.height - box_height) // 2))
#     return left, top, box_width, box_height


def calculate_bounding_box(scale:float =1, height_scale:float =1, width_scale:float =1):
    # Get the size of the screen
    screen_size = QDesktopWidget().screenGeometry(-1)

    # Calculate width and height based on scale
    width = screen_size.width() * scale * width_scale
    height = screen_size.height() * scale * height_scale

    # Calculate left and top coordinates for centering the overlay
    left = (screen_size.width() - width) // 2
    top = (screen_size.height() - height) // 2

    return [int(var) for var in [left, top, width, height]]


class Overlay(QWidget):
    def __init__(self, scale: float=1, height_scale: float=1, width_scale: float=1, border_thickness: int=3):
        super().__init__()

        # Calculate the size and position of the overlay
        left, top, width, height = calculate_bounding_box(scale, height_scale, width_scale)

        # Set the window geometry (position and size)
        self.setGeometry(left, top, width, height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        label = QLabel("")
        label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(label)
        self.setLayout(layout)
        
        self.setStyleSheet(f"border: {border_thickness}px solid yellow; background-color: rgba(0, 0, 0, 0);")

        
class ChatBox(QWidget):
    def __init__(self):
        super().__init__()

        self.messages = []
        self.layout = QVBoxLayout() # type: ignore

        # Add the text display area
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.layout.addWidget(self.text_display)

        # Add a text entry field
        self.text_entry = QLineEdit()
        self.text_entry.returnPressed.connect(self.submit_message)
        self.layout.addWidget(self.text_entry)

        self.setLayout(self.layout)

    def submit_message(self):
        message = self.text_entry.text()
        if message:
            self.messages.append(message)
            self.text_display.append(message)
            self.text_entry.clear()
            print(f'New message: {message}')

    def get_new_messages(self):
        return self.messages

    def clear_messages(self):
        self.text_display.clear()
        self.messages = []

if __name__ == '__main__':
    app = QApplication([])

    chatbox = ChatBox()
    chatbox.show()
    
    overlay = Overlay(scale=0.25, height_scale=1, width_scale=1)
    overlay.show()

    app.exec_()