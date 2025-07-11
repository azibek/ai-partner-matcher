# search_agent.py
from typing import List
import httpx
from backend.config import settings
from backend.llm.base import get_llm_client
from loguru import logger

SERP_URL = "https://serpapi.com/search"

def build_search_prompt(product_description: str) -> List[dict]:
    return [
        {"role": "system", "content": "You're an expert research assistant."},
        {"role": "user", "content": f"Given the following product: {product_description}, generate 5 highly specific Google search queries to discover potential strategic partners, distributors, or enterprise customers. The queries should be diverse and include different industries or use cases."}
    ]

async def generate_search_queries(product_description: str) -> List[str]:
    llm = get_llm_client()
    prompt = build_search_prompt(product_description)
    response = await llm.chat(prompt)
    return [q.strip("- ") for q in response.split("\n") if q.strip()]

async def fetch_search_results(query: str, num: int = 5) -> List[str]:
    print(settings.SERP_API_KEY)
    params = {
        "engine": "google",
        "q": query,
        "api_key": settings.SERP_API_KEY,
        "num": num
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(SERP_URL, params=params, timeout=30)
        res.raise_for_status()
        data = res.json()
        return [item.get("link") for item in data.get("organic_results", []) if "link" in item]

async def search_domains(product_description: str) -> List[str]:
    queries = await generate_search_queries(product_description)
    all_links = []
    for q in queries:
        try:
            links = await fetch_search_results(q)
            all_links.extend(links)
        except Exception as e:
            print(f"Search failed for query '{q}': {e}")
    return all_links
