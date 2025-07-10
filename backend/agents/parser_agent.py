import json
import re
from backend.schemas import PartnerMatch

def extract_json_from_llm(response: str) -> str:
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
    return match.group(1) if match else response.strip()

def parse_match_blocks(llm_output: str) -> list[PartnerMatch]:
    try:
        cleaned = extract_json_from_llm(llm_output)
        parsed = json.loads(cleaned)
        return [PartnerMatch(**entry) for entry in parsed]
    except Exception as e:
        print("Failed to parse LLM output:\n", llm_output)
        raise ValueError("LLM output is not valid match data.") from e
