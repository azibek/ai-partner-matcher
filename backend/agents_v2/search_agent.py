# backend/agents/search_agent.py

import re
from abc import ABC, abstractmethod
from typing import List

from playwright.async_api import async_playwright
import logging

logger = logging.getLogger(__name__)

# --- Strategy Interface ---
class SearchEngine(ABC):
    @abstractmethod
    async def search(self, query: str, num: int = 10) -> str:
        pass

# --- Concrete Strategy: Google ---
class GoogleSearchEngine(SearchEngine):
    async def search(self, query: str, num: int = 10) -> str:
        logger.info(f"Searching Google for: {query}")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(f"https://www.google.com/search?q={query}&num={num}")
            await page.wait_for_timeout(5000)
            content = await page.content()
            await browser.close()
            return content

# --- Concrete Strategy: DuckDuckGo ---
class DuckDuckGoSearchEngine(SearchEngine):
    async def search(self, query: str, num: int = 10) -> str:
        import httpx

        url = "https://html.duckduckgo.com/html/"
        params = {"q": query}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }

        async with httpx.AsyncClient() as client:
            res = await client.post(url, data=params, headers=headers)
            res.raise_for_status()
            return res.text

# --- Extractor ---
def extract_urls_from_html(html: str) -> List[str]:
    logger.info("Extracting URLs from HTML content")
    pattern = re.compile(r'https?://[\w./\-_%#?=&]+')
    all_links = re.findall(pattern, html)
    filtered = [link for link in all_links if not link.endswith(".dtd")]
    return list(set(filtered))  # remove duplicates

# --- Future Hook: LLM-Aided Fallback (skeleton) ---
async def llm_categorize_urls(urls: List[str]) -> List[str]:
    # TODO: use LLM to filter + categorize company vs article vs noise
    return urls

# --- Main Agent Class ---
class WebSearchAgent:
    def __init__(self, engine: SearchEngine):
        self.engine = engine

    async def run(self, query: str, num: int = 10) -> List[str]:
        html = await self.engine.search(query, num=num)
        urls = extract_urls_from_html(html)
        categorized = await llm_categorize_urls(urls)
        logger.info(f"Extracted {len(categorized)} URLs")
        return categorized

# --- Example Runtime Switch ---
ENGINE_MAP = {
    "google": GoogleSearchEngine,
    "duckduckgo": DuckDuckGoSearchEngine,
    # "bing": BingSearchEngine,  # Add more later
}

def get_search_agent(engine_name: str = "duckduckgo") -> WebSearchAgent:
    engine_cls = ENGINE_MAP.get(engine_name.lower())
    if not engine_cls:
        raise ValueError(f"Unsupported engine: {engine_name}")
    return WebSearchAgent(engine=engine_cls())
