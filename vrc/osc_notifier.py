from pythonosc import udp_client
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtCore import pyqtSlot, QMutex
import time


class OSCNotifier(QThread):
    song_added_signal = pyqtSignal(str)
    song_already_in_queue_signal = pyqtSignal(str)
    custom_message_signal = pyqtSignal(str)
    clear_chat_signal = pyqtSignal()
    
    def __init__(self, ip="127.0.0.1", port=9000):
        super().__init__()
        self.client = udp_client.SimpleUDPClient(ip, port)
        self.message_queue = []
        self.mutex = QMutex()  # Lock to synchronize access to message_queue
        self.last_song_added = ""
        self.default_message = f"Type: \"@@song name\" in front of me to add a song to queue. Last Song: {self.last_song_added}"
        
        self.song_added_signal.connect(self.on_song_added)
        self.song_already_in_queue_signal.connect(self.on_duplicate_song)
        self.custom_message_signal.connect(self.send_custom_message)
        self.clear_chat_signal.connect(self.clear_chat)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_message_queue)
        self.handle_message_queue()

       
    @pyqtSlot(str)
    def on_duplicate_song(self, song_name):
        self.mutex.lock()
        self.message_queue.append(song_name)
        self.mutex.unlock()
    
    def send_custom_message(self, message):
        self.client.send_message("/chatbox/input", [message,True,False])
    
    def clear_chat(self):
        self.client.send_message("/chatbox/input", ["",True,False])
    
    @pyqtSlot(str)
    def on_song_added(self, message):
        self.mutex.lock()
        self.message_queue.append(message + " added to queue!")
        self.last_song_added = message
        self.mutex.unlock()
        print(message + " added to queue!")

    def handle_message_queue(self):
        if self.message_queue:
            self.send_custom_message(self.message_queue.pop(0))
            self.timer.start(5000)
        else:
            self.display_default_message()
            self.timer.start(5000)

    def display_default_message(self):
        self.send_custom_message(self.default_message)
