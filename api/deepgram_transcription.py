import asyncio
import aiohttp
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from config import Config
from utils import BaseAPIClient, logger

class DeepgramTranscriptionClient(BaseAPIClient):
    def __init__(self):
        super().__init__(Config.DEEPGRAM_API_KEY)
        self.client = DeepgramClient(self.api_key)

    async def start_transcription(self, audio_url: str) -> None:
        try:
            dg_connection = await self.client.listen.live.v("1")

            async def on_message(self, result, **kwargs):
                sentence = result.channel.alternatives[0].transcript
                if sentence:
                    logger.info(f"Speaker: {sentence}")

            async def on_metadata(self, metadata, **kwargs):
                logger.info(f"Metadata: {metadata}")

            async def on_error(self, error, **kwargs):
                logger.error(f"Deepgram error: {error}")

            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
            dg_connection.on(LiveTranscriptionEvents.Error, on_error)

            options = LiveOptions(
                model="nova-2",
                language="en-US",
                smart_format=True,
            )

            await dg_connection.start(options)

            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as response:
                    while True:
                        chunk = await response.content.read(4096)
                        if not chunk:
                            break
                        await dg_connection.send(chunk)

            await dg_connection.finish()
            logger.info("Transcription finished")

        except Exception as e:
            logger.error(f"Could not open socket: {e}")

deepgram_client = DeepgramTranscriptionClient()

async def start_deepgram_transcription(audio_url: str) -> str:
    await deepgram_client.start_transcription(audio_url)
    return "Transcription started"