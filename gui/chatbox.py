from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QApplication, QSlider, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal, QRect
import sys
        
class ChatBox(QWidget):
    new_message_signal = pyqtSignal(str)
    capture_area_updated_signal = pyqtSignal(QRect)
    process_ocr_signal = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.default_screen = QApplication.desktop().screenGeometry()
        self.output_area = QRect()
        self.setupUI()
        self.output_rect()
        self.setGeometry(
            self.output_area.right(),
            self.output_area.center().y() - self.windowHeight // 2,
            self.windowWidth,
            self.windowHeight,
            )

    def setupUI(self):
        self.layout = QVBoxLayout()  # type: ignore
        self.log_display = self.setupLogs()
        self.text_display = self.setupTextEdit()
        self.text_entry = self.setupLineEdit()
        self.rect_scale_slider = self.setupSlider()
        self.windowHeight = 300
        self.windowWidth = 650

        self.setLayout(self.layout)
        self.setWindowTitle("ChatBox")

        self.setStyleSheet(self.getStyleSheet())
        
    def setupLogs(self):
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        log_display.setFixedHeight(100)
        self.layout.addWidget(log_display)
        return log_display
        
    def setupTextEdit(self):
        text_display = QTextEdit()
        text_display.setReadOnly(True)
        self.layout.addWidget(text_display)
        return text_display

    def setupLineEdit(self):
        text_entry = QLineEdit()
        text_entry.setPlaceholderText("Chat away")
        text_entry.returnPressed.connect(self.submit_message)
        self.layout.addWidget(text_entry)
        return text_entry

    def setupSlider(self):
        # Create a horizontal layout
        slider_layout = QHBoxLayout()

        # Create a checkbox
        checkbox = QCheckBox("OCR")
        slider_layout.addWidget(checkbox)
        checkbox.setChecked(True)
        # Output true or false when the checkbox is clicked
        checkbox.stateChanged.connect(lambda: self.process_ocr_signal.emit(checkbox.isChecked()))
        
        # Create a slider
        rect_scale_slider = QSlider(Qt.Horizontal)
        rect_scale_slider.setMinimum(1)
        rect_scale_slider.setMaximum(100)
        rect_scale_slider.setValue(25)
        rect_scale_slider.valueChanged.connect(self.output_rect)
        slider_layout.addWidget(rect_scale_slider)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(slider_layout)

        return rect_scale_slider

    def getStyleSheet(self):
        return """
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
            QCheckBox {
                color: white;
            }
        """

    def submit_message(self):
        message = self.text_entry.text()
        if message:
            self.text_display.append(message)
            self.text_entry.clear()
            self.new_message_signal.emit(message)

    def receive_error(self, error):
        self.log_display.append(error)

    def clear_messages(self):
        self.text_display.clear()
        
    def output_rect(self):
        scale = self.rect_scale_slider.value() / 100
        left = self.default_screen.width() * (1 - scale) / 2
        top = self.default_screen.height() * (1 - scale) / 2
        width = self.default_screen.width() * scale
        height = self.default_screen.height() * scale
        self.output_area = QRect(int(left), int(top), int(width), int(height))
        self.capture_area_updated_signal.emit(self.output_area)
        
if __name__ == '__main__':
    from overlay import Overlay
    app = QApplication(sys.argv)
    chatbox = ChatBox()
    overlay = Overlay(chatbox.output_area)
    chatbox.capture_area_updated_signal.connect(overlay.setGeometry)
    sys.exit(app.exec_())