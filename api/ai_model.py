from groq import Groq
from typing import List, Dict
from config import Config
from utils import BaseAPIClient, logger

class GroqClient(BaseAPIClient):
    def __init__(self):
        super().__init__(Config.GROQ_API_KEY)
        self.client = Groq(api_key=self.api_key)

    async def get_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=messages,
                model="llama3-70b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return self.handle_error(e)

groq_client = GroqClient()

async def get_ai_response(text: str) -> str:
    messages = [
        {"role": "system", "content": "You are an AI designed to engage in prank calls."},
        {"role": "user", "content": text},
    ]
    return await groq_client.get_response(messages)