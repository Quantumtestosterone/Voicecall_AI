import logging
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def handle_error(self, error: Exception) -> str:
        logger.error(f"API Error: {error}")
        return f"Error: {error}"