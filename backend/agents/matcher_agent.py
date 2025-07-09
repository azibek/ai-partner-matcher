from backend.agents.llm_clients import get_llm_client, get_search_client
from backend.schemas import PartnerMatch
import json


import re

llm = get_llm_client()
search = get_search_client()


def extract_json_from_llm_response(response: str) -> str:
    # Remove Markdown-style code fences if present
    code_block = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
    if code_block:
        return code_block.group(1)
    return response.strip()

prompt_template = """
You are an AI assistant that identifies potential strategic partners for B2B products.

Your job is to return a JSON array of 3 company match suggestions.

For each company, include:
- company_name: Name of the company
- domain: Website domain (no https://)
- industry: Industry or sector
- fit_score: Relevance score between 0–100
- decision_maker: Job title of ideal contact person
- contact_email: (if unknown, put "unknown")
- ai_drafted_email: Outreach email message tailored to this company

Product description:
\"\"\"
{product_description}
\"\"\"

Respond with *only valid JSON* — no prose or explanations.
"""


async def generate_matches(product_description: str):
    prompt = prompt_template.replace("{product_description}", product_description)

    messages = [
        {"role": "system", "content": "You are a strategic partnerships AI assistant."},
        {"role": "user", "content": prompt}
    ]

    response = await llm.chat(messages)
    cleaned = extract_json_from_llm_response(response)

    print("LLM RAW RESPONSE:\n", cleaned)
    try:
        parsed = json.loads(cleaned)
        matches = [PartnerMatch(**match) for match in parsed]
        return matches
    except json.JSONDecodeError:
        raise ValueError("LLM response could not be parsed as JSON")
    except Exception as e:
        raise ValueError(f"Unexpected structure in LLM response: {e}")