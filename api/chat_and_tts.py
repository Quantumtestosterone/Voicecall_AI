import asyncio
from .ai_model import get_ai_response, set_ai_model
from .text_to_speech import convert_text_to_speech
from groq import Groq
from config import Config
import tempfile

async def chat_and_speak(user_input: str, system_prompt: str):
    ai_client = set_ai_model("Claude 3.5 Sonnet")
    ai_response = await get_ai_response(ai_client, system_prompt, user_input)
    audio_file = await convert_text_to_speech(ai_response)
    return ai_response, audio_file

async def transcribe_audio(audio_file):
    client = Groq(api_key=Config.GROQ_API_KEY)
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(audio_file.read())
        temp_file_path = temp_file.name

    with open(temp_file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(temp_file_path, file),
            model="whisper-large-v3",
            response_format="text",
            language="en",
        )
    
    return transcription.text