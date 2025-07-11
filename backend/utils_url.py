# url_utils.py
from urllib.parse import urlparse
from typing import List
import tldextract

def extract_root_domain(url: str) -> str:
    parsed = tldextract.extract(url)
    return f"{parsed.domain}.{parsed.suffix}" if parsed.suffix else parsed.domain

def normalize_urls(urls: List[str]) -> List[str]:
    roots = {extract_root_domain(url) for url in urls if url.startswith("http")}
    return sorted(roots)

def deduplicate_urls(urls: List[str]) -> List[str]:
    return list(set(urls))
