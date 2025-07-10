# backend/agents/web_search_agent.py

import httpx
import os

SERP_API_KEY = os.getenv("SERPAPI_API_KEY")
SERP_API_URL = "https://serpapi.com/search"

async def search_google_domains(query: str, num_results: int = 5) -> list[str]:
    if not SERP_API_KEY:
        raise ValueError("Missing SerpAPI key")

    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": SERP_API_KEY,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(SERP_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

    results = data.get("organic_results", [])
    urls = []

    for result in results:
        url = result.get("link")
        if url:
            domain = extract_root_domain(url)
            if domain not in urls:
                urls.append(domain)

    return urls

def extract_root_domain(url: str) -> str:
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except:
        return url
