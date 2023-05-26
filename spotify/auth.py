import spotipy, os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from PyQt5.QtCore import QThread, pyqtSignal

class SpotifyQThread(QThread):
    
    song_added_to_queue = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.last_song: dict = {}
        self.sp = self.authenticate()
        
    def authenticate(self):

        # Load environment variables from .env file
        load_dotenv()

        # Check for existence of environment variables
        if not os.getenv('SPOTIPY_CLIENT_ID'):
            raise Exception("Environment variable SPOTIPY_CLIENT_ID is not set")

        if not os.getenv('SPOTIPY_CLIENT_SECRET'):
            raise Exception("Environment variable SPOTIPY_CLIENT_SECRET is not set")

        if not os.getenv('SPOTIPY_REDIRECT_URI'):
            raise Exception("Environment variable SPOTIPY_REDIRECT_URI is not set")

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
            scope='user-modify-playback-state,user-read-currently-playing,user-read-playback-state'
        ))
        return sp
    
    def song_search(self, song_name):
        results = self.sp.search(q=song_name, limit=1)
        
        if results:
            song_name_result = results['tracks']['items'][0]['name']
            
            if results['tracks']['items'] and song_name_result != self.last_song:
                song_id = results['tracks']['items'][0]['id']
                song_artist = results['tracks']['items'][0]['artists'][0]['name']
                self.last_song = {song_id:f"{song_name_result} by {song_artist}"}
                self.check_song_in_queue(song_id)
            elif song_name_result == self.last_song:
                print(f"{song_name_result} is already in the queue")
                
        
    def check_song_in_queue(self, song_id):
        queue = self.sp.queue()
        
        if queue:
            if not queue['queue'] and not queue['currently_playing']:
                raise Exception("Please make sure Spotify is open and a song is playing")
            else:
                queue_check = [item['id'] for item in queue['queue']] + [queue['currently_playing']['id']]
                if song_id not in queue_check:
                    self.add_song_to_queue(song_id)
    
    def add_song_to_queue(self, song_id):
        try:
            self.sp.add_to_queue(song_id)
            self.song_added_to_queue.emit(self.last_song[song_id])
        except Exception as e:
            print(f"Error adding song to queue: {e}")

if __name__ == "__main__":
    sp = SpotifyQThread()
    sp.start()
    sp.song_search("psychosocial")
    