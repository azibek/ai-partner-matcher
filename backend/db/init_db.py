# db/init_db.py
from backend.db.base import Base
from backend.db.session import engine
from backend.db.models import Company

def init_db():
    Base.metadata.create_all(bind=engine)
