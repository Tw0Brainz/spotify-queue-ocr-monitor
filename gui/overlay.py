from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QRect


class Overlay(QWidget):
    def __init__(self,initial_area: QRect,border_thickness: int=3):
        super().__init__()

        # Calculate the size and position of the overlay

        # Set the window geometry (position and size)
        self.setGeometry(initial_area)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        layout = QVBoxLayout()
        label = QLabel("")
        label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(label)
        self.setLayout(layout)
        
        self.setStyleSheet(f"border: {border_thickness}px solid yellow; background-color: rgba(0, 0, 0, 0);")
        
        

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    from chatbox import ChatBox
    app = QApplication(sys.argv)
    chatbox = ChatBox()
    overlay = Overlay(chatbox.output_area)
    chatbox.capture_area_updated_signal.connect(overlay.setGeometry)
    sys.exit(app.exec_())
    