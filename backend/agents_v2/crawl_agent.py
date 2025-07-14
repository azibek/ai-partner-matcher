# backend/agents/crawl_agent.py
from backend.agents_v2.content_flattener_agent import extract_company_urls_from_content_pages
from backend.agents_v2.signal_filter import SignalFilterAgent
from typing import List

signal_filter = SignalFilterAgent()
async def finalize_company_urls(company_urls: List[str], content_urls: List[str]) -> List[str]:
    company_urls = await signal_filter.filter(company_urls)
    content_urls = await signal_filter.filter(content_urls)

    extracted_from_articles = await extract_company_urls_from_content_pages(content_urls)
    all_urls = deduplicate_urls(company_urls + extracted_from_articles)

    return all_urls
def deduplicate_urls(urls: List[str]) -> List[str]:
    """
    Normalize and deduplicate a list of URLs.

    Args:
        urls (List[str]): List of URL strings.

    Returns:
        List[str]: Deduplicated list of normalized URLs.
    """
    seen = set()
    deduped = []
    for url in urls:
        norm = url.strip().lower().rstrip("/")
        if norm not in seen:
            seen.add(norm)
            deduped.append(url)
    return deduped