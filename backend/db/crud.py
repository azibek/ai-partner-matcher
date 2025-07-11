# db/crud.py
from sqlalchemy.orm import Session
from backend.db import models
from typing import Optional, List

def get_company_by_domain(db: Session, domain: str) -> Optional[models.Company]:
    return db.query(models.Company).filter(models.Company.domain == domain).first()

def create_company(db: Session, data: dict) -> models.Company:
    db_company = models.Company(**data)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def upsert_company(db: Session, data: dict) -> models.Company:
    existing = get_company_by_domain(db, data["domain"])
    if existing:
        for key, value in data.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        return create_company(db, data)

def list_companies(db: Session, limit: int = 100) -> List[models.Company]:
    return db.query(models.Company).limit(limit).all()
