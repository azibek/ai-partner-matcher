# backend/agents/company_extractor_agent.py

"""
Module: company_extractor_agent

This module contains functionality to crawl a list of article/content page URLs,
extract links from them, and identify possible company website URLs. It is a 
key step in flattening content-type sources (like blog posts or listings) into
direct company websites for further crawling or enrichment.
"""

import re
from typing import List, Set
from bs4 import BeautifulSoup
import httpx
from loguru import logger
from backend.agents.utils.clean_html import clean_html_for_llm


# Basic regex to extract URLs from HTML/text
URL_REGEX = r"https?://[^\s\"'<>]+"

def extract_links_from_html(html: str) -> Set[str]:
    """
    Extract all hyperlinks from the given HTML content.

    Args:
        html (str): Raw HTML content.

    Returns:
        Set[str]: A set of unique URLs found in anchor tags.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = str(a_tag.get("href"))
        if href.startswith("http"):
            links.add(href)
    return links

def filter_possible_company_urls(urls: Set[str]) -> List[str]:
    """
    Filter out non-company URLs based on domain heuristics and URL structure.

    Args:
        urls (Set[str]): Set of extracted URLs.

    Returns:
        List[str]: List of URLs that are likely to point to company homepages.
    """
    filtered = [
        url for url in urls
        if not any(domain in url for domain in [
            "linkedin.com", "twitter.com", "facebook.com", "youtube.com", "wikipedia.org"
        ]) and len(url.split("/")) <= 5 and not url.endswith((".pdf", ".jpg", ".png", ".svg", ".zip"))
    ]
    return list(filtered)

async def extract_company_urls_from_content_pages(content_urls: List[str]) -> List[str]:
    """
    Asynchronously fetch a list of content URLs and extract potential company links from them.

    Args:
        content_urls (List[str]): A list of article or content page URLs.

    Returns:
        List[str]: A deduplicated, sorted list of likely company URLs extracted from those pages.
    """
    extracted_urls = set()

    async with httpx.AsyncClient(timeout=15) as client:
        for url in content_urls:
            try:
                logger.info(f"Crawling content URL: {url}")
                res = await client.get(url, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
                res.raise_for_status()

                html = res.text
                clean_html = clean_html_for_llm(html)
                raw_links = extract_links_from_html(clean_html)
                filtered = filter_possible_company_urls(raw_links)

                logger.info(f"Found {len(filtered)} possible company URLs from {url}")
                extracted_urls.update(filtered)

            except Exception as e:
                logger.warning(f"Failed to crawl {url}: {e}")

    return sorted(extracted_urls)
