async def search_song(sp, song_name):
    """Search for a song on Spotify.

    Args:
        sp: spotipy.Spotify object
        song_name: Name of the song to search for

    Returns:
        song_id: The Spotify ID of the song, or None if no song was found
    """
    results = sp.search(q=song_name, limit=1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['id'], results['tracks']['items'][0]['name']

    return None, None


async def check_song_in_queue(sp, song_id):
    """Check if a song is already in the user's queue.

    Args:
        sp: spotipy.Spotify object
        song_id: The Spotify ID of the song

    Returns:
        True if the song is in the queue, False otherwise
    """
    
    # Generate a list of the user's queue items and check the song ID against it
    queue = sp.queue()
    queue_check = [item['id'] for item in queue['queue']]
    queue_check.append(queue['currently_playing']['id'])
    return song_id in queue_check


async def add_song_to_queue(sp, song_id):
    """Add a song to the user's queue.

    Args:
        sp: spotipy.Spotify object
        song_id: The Spotify ID of the song
    """
    sp.add_to_queue(song_id)
