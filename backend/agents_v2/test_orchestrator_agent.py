import asyncio
from agents_orchestrator import run_discovery_pipeline

if __name__ == "__main__":
    product = "AI assistant that helps enterprises automate customer support"
    company = "We are looking for innovative partners in SaaS, customer experience, or automation sectors."

    asyncio.run(run_discovery_pipeline(product, company))