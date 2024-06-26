import anthropic
from groq import Groq
from typing import List, Dict
from config import Config
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnthropicClient:
    def __init__(self):
        self.api_key = Config.ANTHROPIC_API_KEY
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    async def get_response(self, messages: List[Dict[str, str]], system_prompt: str) -> str:
        try:
            if not self.api_key:
                logger.error("Anthropic API key is not set")
                return "Error: Anthropic API key is not set"

            logger.info(f"Sending request to Anthropic API with system prompt: {system_prompt}")
            response = await asyncio.to_thread(
                self.client.messages.create,
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                temperature=0,
                system=system_prompt,
                messages=[{"role": m["role"], "content": m["content"]} for m in messages if m["role"] == "user"]
            )
            logger.info("Received response from Anthropic API")
            return response.content[0].text
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return f"Anthropic API error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in Anthropic client: {str(e)}")
            return f"Unexpected error: {str(e)}"

class GroqClient:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = Groq(api_key=self.api_key)
        return self._client

    async def get_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            if not self.api_key:
                logger.error("Groq API key is not set")
                return "Error: Groq API key is not set"

            logger.info("Sending request to Groq API")
            chat_completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                messages=messages,
                model="llama3-70b-8192",  # Verify this model name
                temperature=0,
                max_tokens=1000,
            )
            logger.info("Received response from Groq API")
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in Groq client: {str(e)}")
            return f"Error: {str(e)}"

def set_ai_model(model: str):
    if model == "Groq":
        return GroqClient()
    elif model == "Claude 3.5 Sonnet":
        return AnthropicClient()
    else:
        raise ValueError("Invalid AI model selected")

async def get_ai_response(client, system_prompt: str, text: str) -> str:
    messages = [
        {"role": "user", "content": text},
    ]
    if isinstance(client, AnthropicClient):
        return await client.get_response(messages, system_prompt)
    else:
        messages.insert(0, {"role": "system", "content": system_prompt})
        return await client.get_response(messages)