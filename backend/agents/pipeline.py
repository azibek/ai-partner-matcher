# pipeline.py

from typing import List

from backend.agents.search_agent import generate_search_queries
from backend.agents.search_agent import search_domains
from backend.agents.crawl_agent import crawl_company
from backend.agents.html_info_extracter_agent import extract_company_info
from backend.db.crud import upsert_company
from backend.db.session import SessionLocal
from backend.db.models import Company
from backend.agents.utils.util_gsearch import fetch_duckduckgo_results

from loguru import logger


async def run_discovery_pipeline(product_description: str) -> List[Company]:
    db = SessionLocal()
    try:
        logger.info("Generating search queries from product description")
        queries = await generate_search_queries(product_description)

        logger.info(f"Generated queries: {queries}")
        all_domains = set()
        for query in queries:
            logger.info(f"Searching domains for: {query}")
            domains = await fetch_duckduckgo_results(query)
            logger.info(f"Found {len(domains)} domains")
            all_domains.update(domains)

        results = []
        for domain in all_domains:
            logger.info(f"Crawling domain: {domain}")
            html = await crawl_company(domain)
            if not html:
                logger.warning(f"Skipping {domain} due to empty crawl result")
                continue

            logger.info(f"Extracting company info from {domain}")
            company_data = await extract_company_info(html, domain)
            if not company_data:
                logger.warning(f"No company info extracted from {domain}")
                continue

            logger.info(f"Upserting company info for {company_data.name}")
            db_company = upsert_company(db, company_data)
            results.append(db_company)

        return results
    finally:
        db.close()
