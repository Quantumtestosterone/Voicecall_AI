import asyncio
import aiohttp
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepgramTranscriptionClient:
    def __init__(self):
        self.api_key = Config.DEEPGRAM_API_KEY
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = DeepgramClient(self.api_key)
        return self._client

    async def start_transcription(self, audio_file) -> str:
        try:
            transcription = await self.client.transcription.prerecorded.v1.transcribe_file(
                audio_file, 
                options={"model": "nova-2", "language": "en-US", "smart_format": True}
            )
            return transcription.results.channels[0].alternatives[0].transcript
        except Exception as e:
            logger.error(f"Could not process audio: {e}")
            return f"Error during transcription: {str(e)}"

async def start_deepgram_transcription(audio_file) -> str:
    client = DeepgramTranscriptionClient()
    return await client.start_transcription(audio_file)