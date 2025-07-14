from bs4 import BeautifulSoup

def clean_html_for_llm(html: str, max_chars: int = 4000) -> str:
    soup = BeautifulSoup(html, "html.parser")

    parts = []

    # Extract text from common informative tags
    for tag in ["title", "h1", "h2", "p", "meta", "footer"]:
        for element in soup.find_all(tag):
            text = element.get_text(strip=True)
            if text:
                parts.append(text)

    # Extract all anchor tag links (http, https, mailto)
    for a_tag in soup.find_all("a", href=True):
        link_text = a_tag.get_text(strip=True)
        href = str(a_tag["href"])
        if href.startswith("http") or href.startswith("mailto:"):
            formatted = f"{link_text} ({href})" if link_text else href
            parts.append(formatted)

    combined = "\n".join(parts)
    return combined[:max_chars]
