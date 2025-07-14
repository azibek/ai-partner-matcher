# backend/agents_v2/pipeline.py

from typing import List, Dict
from loguru import logger

from backend.agents_v2.query_builder import LLMQueryBuilder
from backend.agents_v2.search_agent import get_search_agent
from backend.agents_v2.signal_filter import SignalFilterAgent
from backend.agents_v2.company_classifier import CompanyClassifierAgent
from backend.agents_v2.content_flattener_agent import extract_company_urls_from_content_pages
from backend.agents_v2.info_extraction_agent import InfoExtractionAgent
from backend.agents_v2.crawl_agent import deduplicate_urls


async def run_discovery_pipeline_v2(product_desc: str, company_desc: str) -> List[Dict]:
    logger.info("🔍 Starting partner discovery pipeline...")

    # 1. Query Generation
    query_builder = LLMQueryBuilder()
    queries = await query_builder.build_queries(product=product_desc, company=company_desc)
    logger.success(f"✅ Generated {len(queries)} search queries")

    # 2. Web Search
    search_agent = get_search_agent(engine_name="duckduckgo")  # <- updated usage
    raw_urls = []
    for query in queries:
        result = await search_agent.run(query, 2)
        raw_urls.extend(result)

    logger.success(f"🌐 Found {len(raw_urls)} raw URLs from search results")

    

    # 3. Signal Filtering
    signal_filter = SignalFilterAgent()
    high_signal_urls = await signal_filter.filter(raw_urls)
    logger.success(f"📈 Retained {len(high_signal_urls)} high-signal URLs")

    # 4. Company vs Content Classification
    classifier = CompanyClassifierAgent()
    company_urls, content_urls = await classifier.classify(high_signal_urls)
    logger.success(f"🏢 {len(company_urls)} company URLs | 📄 {len(content_urls)} content URLs")

    # 5. Content Flattening: Extract more company URLs
    extracted_company_urls = await extract_company_urls_from_content_pages(content_urls)
    all_company_urls = deduplicate_urls(company_urls + extracted_company_urls)
    logger.success(f"🔁 Final deduplicated company URLs: {len(all_company_urls)}")

    # 6. Info Extraction
    
    extractor = InfoExtractionAgent()
    company_profiles = []
    for url in all_company_urls:
        try:
            profile = await extractor.extract_from_url(url)
            if profile:
                company_profiles.append(profile)
        except Exception as e:
            logger.warning(f"❌ Failed to extract from {url}: {e}")
    logger.success(f"📄 Extracted metadata for {len(company_profiles)} companies")

    return company_profiles
