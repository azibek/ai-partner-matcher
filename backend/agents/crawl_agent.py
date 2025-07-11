# crawler.py
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import asyncio
from backend.config import settings

class CompanyProfile:
    def __init__(self, name=None, description=None, contact_links=None):
        self.name = name
        self.description = description
        self.contact_links = contact_links or []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "contact_links": self.contact_links
        }

async def fetch_html(url: str, timeout: int = settings.CRAWLER_TIMEOUT) -> str:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml"
            }

            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return ""

def extract_base_info(html: str, base_url: str) -> CompanyProfile:
    soup = BeautifulSoup(html, "html.parser")

    # Title or meta og:title as name
    name = soup.title.string.strip() if soup.title else None
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        name = og_title["content"].strip()

    # Meta description or og:description
    description = None
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()
    og_desc = soup.find("meta", property="og:description")
    if og_desc and og_desc.get("content"):
        description = og_desc["content"].strip()

    # Look for contact/about/careers links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if any(kw in href for kw in ["contact", "about", "team", "careers"]):
            abs_url = urljoin(base_url, href)
            links.append(abs_url)

    return CompanyProfile(name=name, description=description, contact_links=list(set(links)))


async def crawl_company(url: str) -> str:
    return await fetch_html(url)
    if not html:
        return CompanyProfile()
    return extract_base_info(html, url)


# Example usage:
# asyncio.run(crawl_company("https://example.com"))
