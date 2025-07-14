# backend/agents/company_classifier.py

from typing import List, Literal, Tuple
from backend.llm.base import get_llm_client

Classification = Literal["company", "content"]

SYSTEM_PROMPT = (
    "You are a classification assistant helping to decide whether a given URL belongs to a COMPANY website "
    "or an informational CONTENT site (e.g. blogs, articles, directories).\n\n"
    "Return only 'company' or 'content' for each item based strictly on the domain name or known usage.\n"
    "Don't try to invent company names or hallucinate content.\n"
    "Examples:\n"
    "- 'https://techcrunch.com/ai-startup-list/' → content\n"
    "- 'https://www.ibm.com' → company\n"
    "- 'https://www.medium.com/some-blog' → content\n"
    "- 'https://openai.com' → company\n"
    "Keep it very strict — if unsure, classify as 'content'.\n"
)

USER_PROMPT_TEMPLATE = "Classify these URLs:\n" + "\n".join("{url}" for url in [])

# from typing import List, Tuple
# from backend.llm.base import get_llm_client

# SYSTEM_PROMPT = (
#     "You are a research assistant classifying URLs from a web search. "
#     "For each URL, decide whether it is a company website (homepage, product, about pages, etc.) "
#     "or a content site (blogs, news, PDFs, etc.). "
#     "Return the labels in order, one per line, with either 'company' or 'content'."
# )

class CompanyClassifierAgent:
    def __init__(self):
        self.llm = get_llm_client()

    async def classify(self, urls: List[str]) -> Tuple[List[str], List[str]]:
        prompt = "Classify these URLs:\n" + "\n".join(urls)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        response = await self.llm.chat(messages)

        raw_lines = [line.strip().lower() for line in response.split("\n") if line.strip()]
        labels = ["content" if "content" in line else "company" for line in raw_lines]
        # labels = [label if label in ("company", "content") else "content" for label in raw_lines]

        company_urls = [url for url, label in zip(urls, labels) if label == "company"]
        content_urls = [url for url, label in zip(urls, labels) if label == "content"]

        return company_urls, content_urls

