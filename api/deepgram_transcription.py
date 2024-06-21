import asyncio
import aiohttp
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from config import Config
from utils import BaseAPIClient, logger

class DeepgramTranscriptionClient(BaseAPIClient):
    def __init__(self):
        super().__init__(Config.DEEPGRAM_API_KEY)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = DeepgramClient(self.api_key)
        return self._client

    async def start_transcription(self, audio_url: str) -> None:
        try:
            # Create a websocket connection to Deepgram
            dg_connection = await self.client.listen.live.v("1")

            # Define the event handlers for the connection
            async def on_message(self, result, **kwargs):
                sentence = result.channel.alternatives[0].transcript
                if sentence:
                    logger.info(f"Speaker: {sentence}")

            async def on_metadata(self, metadata, **kwargs):
                logger.info(f"Metadata: {metadata}")

            async def on_error(self, error, **kwargs):
                logger.error(f"Deepgram error: {error}")

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
            await dg_connection.start(options)

            # Stream the audio to Deepgram
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as response:
                    while True:
                        chunk = await response.content.read(4096)
                        if not chunk:
                            break
                        await dg_connection.send(chunk)

            # Close the connection to Deepgram
            await dg_connection.finish()
            logger.info("Transcription finished")

        except Exception as e:
            logger.error(f"Could not open socket: {e}")
            raise

async def start_deepgram_transcription(audio_url: str) -> str:
    client = DeepgramTranscriptionClient()
    try:
        await client.start_transcription(audio_url)
        return "Transcription started successfully"
    except Exception as e:
        return f"Error starting transcription: {str(e)}"

# For testing purposes
if __name__ == "__main__":
    async def test_transcription():
        test_audio_url = "https://example.com/audio.wav"  # Replace with a real audio URL
        result = await start_deepgram_transcription(test_audio_url)
        print(result)

    asyncio.run(test_transcription())