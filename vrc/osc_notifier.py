from pythonosc import udp_client, dispatcher, osc_server
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, pyqtSlot, QMutex
from PyQt5.QtWidgets import QWidget
from pythonosc.udp_client import SimpleUDPClient

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
        self.default_message = f"Type: \"#song name\" in front of me to add a song to queue. Last Song: {self.last_song_added}"
        
        self.song_added_signal.connect(self.on_song_added)
        self.custom_message_signal.connect(self.send_custom_message)
        self.clear_chat_signal.connect(self.clear_chat)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_message_queue)
        self.handle_message_queue()

    
    @pyqtSlot(str)
    def send_custom_message(self, message):
        self.mutex.lock()
        self.message_queue.append(message)
        self.mutex.unlock()
    
    @pyqtSlot(str)
    def on_song_added(self, message):
        self.mutex.lock()
        self.message_queue.append(message + " added to queue!")
        self.last_song_added = message
        self.default_message = f"Type: \"#song name\" in front of me to add a song to queue. Last Song: {self.last_song_added}"
        self.mutex.unlock()
        print(message + " added to queue!")

    def handle_message_queue(self):
        if self.message_queue:
            self.display_message(self.message_queue.pop(0))
            self.timer.start(5000)
        else:
            self.display_default_message()
            self.timer.start(2500)

    def display_default_message(self):
        self.display_message(self.default_message)

    def display_message(self, message):
        self.client.send_message("/chatbox/input", [message,True,False])
    
    def clear_chat(self):
        self.client.send_message("/chatbox/input", ["",True,False])
        
class OSCListener(QThread):
    def __init__(self, ip="127.0.0.1", port=9001):
        super().__init__()
        self._dispatcher = dispatcher.Dispatcher()
        self._dispatcher.map("/*", self.print_all)
        
        self._server = osc_server.ThreadingOSCUDPServer((ip, port), self._dispatcher)
        print("Serving on {}".format(self._server.server_address))
        
    def print_all(self, address, *args):
        print(f"OSC message received on {address} with arguments: {args}")

    def serve_forever(self):
        self._server.serve_forever()
        
class AvatarParameterChanger(QWidget):
    def __init__(self):
        super().__init__()
        self.parameters = {
            "huehair" : [1.0, 0.43],
            "hueHighlights" : [1.0, 0.43],
            "huetats" : [1.0, 0.43],
            "hueclothes1" : [1.0, 0.43],
            "hueclothes2" : [1.0, 0.43],
            "hueMetal" : [1.0, 0.43],
            
        }
        self.client = SimpleUDPClient("127.0.0.1", 9000)

    def temporary_change_parameters(self):
        for key, values in self.parameters.items():
            self.send_osc_message(key, values[1])
        
        # Set a timer to reset parameters after duration
        QTimer.singleShot(int(2.5 * 1000), self.reset_parameters_to_default)

    def reset_parameters_to_default(self):
        for key, values in self.parameters.items():
            self.send_osc_message(key, values[0])

    def send_osc_message(self, address: str, value: float):
        self.client.send_message("/avatar/parameters/"+address, value)
        
if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    # listener = OSCListener()
    param_changer = AvatarParameterChanger()
    param_changer.temporary_change_parameters()
    # listener.serve_forever()
    app.exec_()
    
  