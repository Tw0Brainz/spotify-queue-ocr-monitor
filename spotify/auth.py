import spotipy, os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

def authenticate():
    """Authenticate with Spotify API.

    Returns:
        sp: spotipy.Spotify object
    """
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