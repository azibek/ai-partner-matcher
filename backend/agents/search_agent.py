import os
import httpx

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

async def search_domains(product_description: str, top_k=5) -> list[str]:
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": f"{product_description} B2B startups",
        "api_key": SERPAPI_API_KEY,
        "num": top_k
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        res.raise_for_status()
        results = res.json()
        return [
            r["link"] for r in results.get("organic_results", []) if "link" in r
        ]
