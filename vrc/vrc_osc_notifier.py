from pythonosc import udp_client

class OSCNotifier:
    def __init__(self, ip="127.0.0.1", port=9000):
        self.client = udp_client.SimpleUDPClient(ip, port)

    def notify_song_added(self, song_name):
        self.client.send_message("/chatbox/input", [f'{song_name} added to queue!',True,False])
        
    def notify_song_already_in_queue(self, song_name):
        self.client.send_message("/chatbox/input", [f'{song_name} is already in the queue!',True,False])
        
    def send_custom_message(self, message):
        self.client.send_message("/chatbox/input", [message,True,False])
        
    def clear_chat(self):
        self.client.send_message("/chatbox/input", ["",True,False])
