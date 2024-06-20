import anthropic
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

class AnthropicClient(BaseAPIClient):
    def __init__(self):
        super().__init__(Config.ANTHROPIC_API_KEY)
        self.client = anthropic.Anthropic(api_key=self.api_key)

    async def get_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                temperature=0,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            return self.handle_error(e)

groq_client = GroqClient()
anthropic_client = AnthropicClient()

def set_ai_model(model: str):
    if model == "Groq":
        return groq_client
    elif model == "Claude 3.5 Sonnet":
        return anthropic_client
    else:
        raise ValueError("Invalid AI model selected")

async def get_ai_response(client, system_prompt: str, text: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]
    return await client.get_response(messages)