def search_song(sp, song_name):
    """Search for a song on Spotify.

    Args:
        sp: spotipy.Spotify object
        song_name: Name of the song to search for

    Returns:
        song_id: The Spotify ID of the song, or None if no song was found
    """
    try:
        results = sp.search(q=song_name, limit=1)
    except Exception as e:
        print(f"Error searching for {song_name}: {e}")
        return None, None
    
    if results['tracks']['items']:
        song_id = results['tracks']['items'][0]['id']
        song_name = results['tracks']['items'][0]['name']
        song_artist = results['tracks']['items'][0]['artists'][0]['name']
        return song_id, f"{song_name} by {song_artist}"
    else:
        return None, None


def check_song_in_queue(sp, song_id):
    """Check if a song is already in the user's queue. This will throw an error if the user is not playing a song and their queue is empty.

    Args:
        sp: spotipy.Spotify object
        song_id: The Spotify ID of the song

    Returns:
        True if the song is in the queue, False otherwise
    """
    
    # Generate a list of the user's queue items and check the song ID against it
    queue = sp.queue()

    if not queue['queue'] and not queue['currently_playing']:
        raise Exception("Please make sure Spotify is open and a song is playing")
    
    queue_check = [item['id'] for item in queue['queue']] + [queue['currently_playing']['id']]
    
    return song_id in queue_check


def add_song_to_queue(sp, song_id):
    """Add a song to the user's queue.

    Args:
        sp: spotipy.Spotify object
        song_id: The Spotify ID of the song
    """
    try:
        sp.add_to_queue(song_id)
    except Exception as e:
        print(f"Error adding song to queue: {e}")
        print(sp.current_playback())
        return
