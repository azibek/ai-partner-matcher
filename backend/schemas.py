from pydantic import BaseModel


class ProductInput(BaseModel):
    product_description: str

class PartnerMatch(BaseModel):
    company_name: str
    domain: str
    industry: str
    fit_score: float
    decision_maker: str
    contact_email: str
    ai_drafted_email: str

class DiscoveryInput(BaseModel):
    product_description: str
    company_description: str = ""