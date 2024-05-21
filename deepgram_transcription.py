import os
import httpx
import threading
from dotenv import load_dotenv
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

load_dotenv()

API_KEY = os.getenv("DG_API_KEY")

def start_deepgram_transcription(audio_url):
    try:
        # Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.listen.live.v("1")

        # Define the event handlers for the connection
        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

        def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        # Register the event handlers
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        # Configure Deepgram options for live transcription
        options = LiveOptions(
            model="nova-2", 
            language="en-US", 
            smart_format=True,
        )

        # Start the connection
        dg_connection.start(options)

        # Create a lock and a flag for thread synchronization
        lock_exit = threading.Lock()
        exit = False

        # Define a thread that streams the audio and sends it to Deepgram
        def myThread():
            with httpx.stream("GET", audio_url) as r:
                for data in r.iter_bytes():
                    lock_exit.acquire()
                    if exit:
                        break
                    lock_exit.release()

                    dg_connection.send(data)

        # Start the thread
        myHttp = threading.Thread(target=myThread)
        myHttp.start()

        # Wait for user input to stop recording
        input("Press Enter to stop recording...\n\n")

        # Set the exit flag to True to stop the thread
        lock_exit.acquire()
        exit = True
        lock_exit.release()

        # Wait for the thread to finish
        myHttp.join()

        # Close the connection to Deepgram
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return
