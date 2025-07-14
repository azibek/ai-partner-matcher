# backend/agents/query_builder.py

from typing import List
from abc import ABC, abstractmethod
from loguru import logger
from backend.config import settings
from backend.llm.base import get_llm_client

SYSTEM_PROMPT = (
    "You are a strategic research assistant helping to discover potential partner companies. "
    "Given a product and company description, generate highly specific, filter-aware Google search queries."
    "Ensure each query targets one of the following intents:"
    "1. Direct company discovery (e.g., 'top [industry] startups for enterprise partnerships')"
    "2. Articles/blogs listing relevant companies (e.g., 'AI companies enabling product innovation site:techcrunch.com')"
    "Use operators like 'site:', 'inurl:', 'intitle:' if helpful. Ensure high precision."
)

USER_PROMPT_TEMPLATE = (
    "Product Description:\n{product}\n"
    "Company Description:\n{company}\n"
    "Return 5 distinct and precise search queries."
)

class QueryBuilder(ABC):
    @abstractmethod
    async def build_queries(self, product: str, company: str) -> List[str]:
        pass

class LLMQueryBuilder(QueryBuilder):
    def __init__(self):
        self.llm = get_llm_client()

    async def build_queries(self, product: str, company: str, num: int = 2) -> List[str]:
        prompt = USER_PROMPT_TEMPLATE.format(product=product, company=company)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        logger.info("Generating search queries using LLM...")
        response = await self.llm.chat(messages)
        queries = [line.strip("- ") for line in response.split("\n") if line.strip()]

        # Filter basic noise (empty lines, too short, no keywords)
        queries = [q for q in queries if len(q) > 10 and any(k in q.lower() for k in ["company", "startups", "innovation", "partner"])]
        logger.info(f"Generated {len(queries)} refined queries")

        final_query = []

        for i in range(num):
            if i > 10:
                break
            final_query.append(queries[i])

        return queries
