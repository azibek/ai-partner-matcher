from backend.agents.llm_clients import get_llm_client
llm = get_llm_client()

async def summarize_companies(urls: list[str], product_description: str) -> list[str]:
    messages = [
        {"role": "system", "content": "You are a partner-matching assistant."},
        {"role": "user", "content": f"""
Given the following product description and these companies:

Product: {product_description}

Companies:
{chr(10).join(urls)}

Return a JSON array of partner suggestions. Each object should include:
- company_name
- domain
- industry
- fit_score
- decision_maker
- contact_email
- ai_drafted_email

Respond with ONLY valid JSON (no markdown formatting).
"""}
    ]
    return await llm.chat(messages)
