# db/models.py
from sqlalchemy import Column, Integer, String, Float
from backend.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    domain = Column(String, unique=True, index=True)
    industry = Column(String)
    contact_email = Column(String)
    contact_person = Column(String)
    fit_score = Column(Float)
    raw_html_path = Column(String)  # optional: file path to raw HTML snapshot
