import aiohttp
from config import Config
from utils import BaseAPIClient, logger

class ElevenLabsClient(BaseAPIClient):
    def __init__(self):
        super().__init__(Config.ELEVENLABS_API_KEY)
        self.voice_id = Config.ELEVENLABS_VOICE_ID

    async def convert_text_to_speech(self, text: str) -> str:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
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
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        with open("output.mp3", "wb") as f:
                            f.write(await response.read())
                        return "output.mp3"
                    else:
                        return f"Error: {response.status} - {await response.text()}"
        except Exception as e:
            return self.handle_error(e)

eleven_labs_client = ElevenLabsClient()

async def convert_text_to_speech(text: str) -> str:
    return await eleven_labs_client.convert_text_to_speech(text)