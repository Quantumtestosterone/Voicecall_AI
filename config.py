import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_API_KEY = os.getenv("TWILIO_API_KEY")
    TWILIO_API_SECRET = os.getenv("TWILIO_API_SECRET")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    DEEPGRAM_API_KEY = os.getenv("DG_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    @classmethod
    def save_to_file(cls):
        config_data = {key: getattr(cls, key) for key in cls.__annotations__}
        with open('config.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    @classmethod
    def load_from_file(cls):
        try:
            with open('config.json', 'r') as f:
                config_data = json.load(f)
            for key, value in config_data.items():
                setattr(cls, key, value)
        except FileNotFoundError:
            pass  # No saved config file yet