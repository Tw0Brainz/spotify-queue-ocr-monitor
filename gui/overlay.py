from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
import os,sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from util.utils import calculate_bounding_box

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
        
        self.show()

        
class ChatBox(QWidget):
    new_message_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()

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
        
        self.setGeometry(500,500,480,240)
        
        self.setStyleSheet("""
            ChatBox {
                background-color: #1e2124;
                border: 1px solid #7289da;
                border-radius: 12px;
                color:#1e2124;
            }
            QTextEdit {
                background-color: #1e2124;
                border: 1px solid #7289da;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
            QLineEdit {
                background-color: #1e2124;
                border: 1px solid #7289da;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
        """)

    def submit_message(self):
        message = self.text_entry.text()
        if message:
            self.text_display.append(message)
            self.text_entry.clear()
            self.new_message_signal.emit(message)
            print(f'New message: {message}')

    def clear_messages(self):
        self.text_display.clear()

if __name__ == '__main__':
    app = QApplication([])

    chatbox = ChatBox()
    chatbox.show()
    
    overlay = Overlay(scale=0.25, height_scale=1, width_scale=1)
    overlay.show()

    app.exec_()