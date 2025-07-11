import httpx
import re
from typing import List

URL_REGEX = re.compile(r'https?://[^\s"\'>]+')

async def fetch_duckduckgo_results(query: str, num: int = 5) -> List[str]:
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url, data=params, headers=headers)
        res.raise_for_status()
        content = res.text

    # Extract URLs from response HTML
    matches = URL_REGEX.findall(content)

    filtered = [
        url for url in matches
        if not url.startswith("https://duckduckgo.com")
        and not url.endswith(".png")
        and "yahoo.com" not in url
        and not url.lower().endswith('dtd')
    ]

    # Deduplicate and limit
    seen = set()
    final = []
    for link in filtered:
        if link not in seen:
            seen.add(link)
            final.append(link)
        if len(final) >= num:
            break

    return final
