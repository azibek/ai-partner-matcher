from .search_agent import search_domains
from .llm_agent import summarize_companies
from .parser_agent import parse_match_blocks

async def generate_matches(product_description: str):
    urls = await search_domains(product_description)
    if not urls:
        return []

    raw_response = await summarize_companies(urls, product_description)
    print("LLM RAW:\n", raw_response)

    matches = parse_match_blocks(raw_response)
    return matches
