import aiohttp
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElevenLabsTTS:
    def __init__(self):
        self.api_key = Config.ELEVENLABS_API_KEY
        self.voice_id = Config.ELEVENLABS_VOICE_ID
        self.base_url = "https://api.elevenlabs.io/v1"

    async def convert_text_to_speech(self, text: str, voice: str = "ElevenLabs") -> str:
        if not self.api_key:
            logger.error("ElevenLabs API key is not set")
            return "Error: ElevenLabs API key is not set"

        if not self.voice_id:
            logger.error("ElevenLabs Voice ID is not set")
            return "Error: ElevenLabs Voice ID is not set"

        url = f"{self.base_url}/text-to-speech/{self.voice_id}/stream"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }

        try:
            logger.info(f"Sending TTS request to ElevenLabs API for text: {text[:50]}...")
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        filename = "output.mp3"
                        with open(filename, "wb") as f:
                            f.write(await response.read())
                        logger.info(f"TTS audio saved as {filename}")
                        return filename
                    else:
                        error_text = await response.text()
                        logger.error(f"ElevenLabs API error: {response.status} - {error_text}")
                        return f"Error: {response.status} - {error_text}"
        except Exception as e:
            logger.error(f"Unexpected error in ElevenLabs TTS: {str(e)}")
            return f"Error: {str(e)}"

async def convert_text_to_speech(text: str, voice: str = "ElevenLabs") -> str:
    tts = ElevenLabsTTS()
    return await tts.convert_text_to_speech(text, voice)