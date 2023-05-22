import asyncio
from ocr.capture import capture_screen
from ocr.process import process_image
from spotify.auth import authenticate
from spotify.api import search_song, check_song_in_queue, add_song_to_queue
from gui.overlay import create_tinker_window, calculate_bounding_box
from vrc.vrc_osc_notifier import OSCNotifier

async def main():
    # authenticate user for Spotify API
    sp = await authenticate()

    # calculate the bounding box parameters
    sleft, stop, box_width, box_height = calculate_bounding_box(0.5)

    # create the overlay window
    root = create_tinker_window(sleft, stop, box_width, box_height,4)
    prev_song_name: str = None
    vrc_notifier = OSCNotifier()
    # begin main loop
    try:
        while True:
            # capture screenshot
            screenshot = capture_screen(sleft, stop, box_width, box_height)

            # process screenshot with OCR to extract song name
            song_name = process_image(screenshot)

            if song_name and (song_name != prev_song_name):
                print(f"Song name detected: {song_name}")

                # search for song on Spotify
                song_id, spotify_song_name = await search_song(sp, song_name)

                if song_id:
                    print(f"Song ID found on Spotify: {song_id}")

                    # check if song is already in queue
                    if not await check_song_in_queue(sp, song_id):
                        print("Adding song to queue...")
                        await add_song_to_queue(sp, song_id)
                        
                        vrc_notifier.notify_song_added(spotify_song_name)
                        prev_song_name = song_name
                    else:
                        print("Song is already in queue!")
                        vrc_notifier.notify_song_already_in_queue(spotify_song_name)

            # update the Tkinter window
            root.update()

            # sleep for 3 seconds
            await asyncio.sleep(3)
            vrc_notifier.clear_chat()
            vrc_notifier.send_custom_message("Type DJREQ: <song name> to request a song!")
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        root.destroy()

if __name__ == "__main__":
    asyncio.run(main())
