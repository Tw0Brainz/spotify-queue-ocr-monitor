import unittest, sys, os, asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spotify.auth import authenticate
from spotify.api import search_song, check_song_in_queue, add_song_to_queue
from ocr.capture import capture_screen
from ocr.process import process_image

class TestOCR(unittest.TestCase):

    def test_image_to_text(self):
        from PIL import Image
        screenshot = capture_screen(0, 0, 100, 100)
        image_path = os.path.join(os.path.dirname(__file__), 'OCR_Test.png')
        screenshot = Image.open(image_path)
        result = process_image(screenshot)
        expected = "never gonna give you up rick astley"
        self.assertEqual(result, expected)

class TestSpotifyAPI(unittest.TestCase):
    
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.sp = self.loop.run_until_complete(authenticate())

    def test_search_song(self):
        result = self.loop.run_until_complete(search_song(self.sp, 'never gonna give you up rick astley'))
        if isinstance(result, tuple):
            song_id = result[0]
        else:
            song_id = result
        # This will pass if 'never gonna give you up rick astley' exists on Spotify
        self.assertIsInstance(song_id, str)

    def test_add_song_to_queue(self):
        # This test is a bit tricky as it depends on the user's Spotify queue
        # We are assuming here that you have a song in your library you can add to the queue
        song_id = '4cOdK2wGLETKBW3PvgPWqT'  # Replace with an actual song ID
        added = self.loop.run_until_complete(add_song_to_queue(self.sp, song_id))
        self.assertIsNone(added)  # add_song_to_queue doesn't return anything, so we expect None

        in_queue = self.loop.run_until_complete(check_song_in_queue(self.sp, song_id))
        self.assertIsNotNone(in_queue)  # check_song_in_queue returns a boolean, so we expect something other than None

if __name__ == "__main__":
    unittest.main()
