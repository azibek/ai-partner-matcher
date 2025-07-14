# extractor.py
from backend.agents.llm_clients import get_llm_client
from typing import Dict
import json
from backend.agents.utils.clean_html import clean_html_for_llm


llm = get_llm_client()

async def extract_company_info(raw_html: str, source_url: str) -> Dict[str, str]:
    clean_html = clean_html_for_llm(raw_html)
    prompt = [
        {"role": "system", "content": "You are an assistant that extracts structured company metadata from web pages."},
        {"role": "user", "content": f"Extract the company details from this HTML snippet. Include fields: company_name, domain, industry, description, contact_email, and headquarters_location. Return JSON only.\nURL: {source_url}\nHTML:\n{clean_html}"}
    ]

    try:

        result = await llm.chat(prompt)
        return json.loads(result)
    except Exception as e:
        print(f"Failed to parse company info: {e}")
        return {}