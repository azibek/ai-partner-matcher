import os
import httpx
from abc import ABC, abstractmethod
from typing import List, Dict
from openai import OpenAI
from ollama import AsyncClient





class LLMClient(ABC):
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        pass

class SearchClient(ABC):
    @abstractmethod
    async def search(self, query: str) -> List[str]:
        pass


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIClient(LLMClient):
    async def chat(self, messages):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    




class LlamaClient(LLMClient):
    def __init__(self, model_name="llama3.1", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.client = AsyncClient(host=base_url)

    async def chat(self, messages):
        response = await self.client.chat(
            model=self.model_name,
            messages=messages  # Same format as OpenAI: [{"role": ..., "content": ...}]
        )
        return response['message']['content'].strip()



class SerpApiClient(SearchClient):
    async def search(self, query: str):
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": 5
        }
        async with httpx.AsyncClient() as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            results = res.json()
            return [
                r.get("link") for r in results.get("organic_results", []) if "link" in r
            ]


def get_llm_client():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    print("provider")
    if provider == "openai":
        return OpenAIClient()
    elif provider == "ollama":
        return LlamaClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

def get_search_client():
    return SerpApiClient()
