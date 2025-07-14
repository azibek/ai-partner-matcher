import json
import re
from typing import List
from backend.llm.base import get_llm_client

URL_REGEX = re.compile(r'https?://[^\s"\'<>]+')

class SignalFilterAgent:
    def __init__(self):
        self.llm = get_llm_client()

    async def filter(self, urls: List[str]) -> List[str]:
        SYSTEM_PROMPT = (
            "You are a research analyst helping identify relevant web pages for discovering strategic partner companies.\n"
            "Classify each URL in the given list as either:\n"
            "- HIGH_SIGNAL: Likely lists or discusses relevant companies, partnerships, or startup ecosystems.\n"
            "- LOW_SIGNAL: Irrelevant, noisy, or unrelated (e.g., personal blogs, generic landing pages).\n"
            "\n"
            "Respond ONLY in this JSON format:\n"
            "{\n"
            '  "high_signal": [{"url": "<URL1>"}, {"url": "<URL2>"}],\n'
            '  "low_signal": [{"url": "<URL3>"}, {"url": "<URL4>"}]\n'
            "}\n"
            "Do not add any other explanation or text. If unsure, classify as LOW_SIGNAL."
        )

        formatted = json.dumps(urls)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": formatted}
        ]

        raw_response = await self.llm.chat(messages)

        try:
            parsed = json.loads(raw_response)
            high_signal_urls = [entry["url"] for entry in parsed.get("high_signal", []) if "url" in entry]
        except json.JSONDecodeError:
            # Fallback: extract all URLs from raw_response
            high_signal_urls = URL_REGEX.findall(raw_response)

        return high_signal_urls[:3]
