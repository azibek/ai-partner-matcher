from abc import ABC, abstractmethod
from typing import List, Dict
import openai
import httpx
from ollama import AsyncClient

from backend.config import settings

class LLMClient(ABC):
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        pass


class OpenAIClient(LLMClient):
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        response = await openai.ChatCompletion.acreate(
            model=settings.MODEL_NAME,
            messages=messages
        )
        return response.choices[0].message.content.strip()




class OllamaClient(LLMClient):
    def __init__(self, model_name="llama3.1", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.client = AsyncClient(host=base_url)

    async def chat(self, messages):
        response = await self.client.chat(
            model=self.model_name,
            messages=messages  # Same format as OpenAI: [{"role": ..., "content": ...}]
        )
        return response['message']['content'].strip()


def get_llm_client() -> LLMClient:
    if settings.LLM_PROVIDER == "openai":
        return OpenAIClient()
    elif settings.LLM_PROVIDER == "ollama":
        return OllamaClient()
    else:
        raise ValueError("Unsupported LLM provider")
