# backend/agents/info_extraction_agent.py

from typing import List, Optional
from pydantic import BaseModel
from bs4 import BeautifulSoup
import httpx
from loguru import logger
from backend.llm.base import get_llm_client


class CompanyInfo(BaseModel):
    url: str
    name: Optional[str] = None
    description: Optional[str] = None
    focus_area: Optional[str] = None
    contact_email: Optional[str] = None
    linkedin: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class InfoExtractionAgent:
    def __init__(self):
        self.llm = get_llm_client()

    async def extract_from_url(self, url: str) -> Optional[CompanyInfo]:
        logger.info(f"Extracting info from: {url}")

        try:
            async with httpx.AsyncClient(timeout=20) as client:
                res = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                res.raise_for_status()
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        raw_text = soup.get_text(" ", strip=True)[:8000]  # LLM input size control

        SYSTEM_PROMPT = (
            "You are a B2B analyst helping craft warm email pitches for strategic partnerships."
            " Given a website's raw text, extract key information about the company."
            " Focus on what's useful to understand and pitch them, including:\n"
            " - Company name\n - Area of focus\n - Short description\n - Contact email\n - Phone or address\n - LinkedIn or team page (if found)."
            " Return only in JSON format: {name, description, focus_area, contact_email, phone, linkedin, address}"
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"URL: {url}\nText:\n{raw_text}"},
        ]

        try:
            response = await self.llm.chat(messages)
            data = self.safe_json_parse(response)
            return CompanyInfo(url=url, **data)
        except Exception as e:
            logger.warning(f"LLM failed on {url}: {e}")
            return None

    def safe_json_parse(self, raw: str) -> dict:
        import json
        try:
            return json.loads(raw)
        except Exception:
            fixed = raw.strip().split("```json")[-1].split("```")[-2].strip()
            return json.loads(fixed)

    async def batch_extract(self, urls: List[str]) -> List[CompanyInfo]:
        results: List[CompanyInfo] = []
        for url in urls:
            info = await self.extract_from_url(url)
            if info:
                results.append(info)
        return results
