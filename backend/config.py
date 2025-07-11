# config.py
import os
from dotenv import load_dotenv
from loguru import logger

class Settings:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.SERP_API_KEY = os.getenv("SERP_API_KEY", "1f7363c25352f0fdfe253f35b140b3676caa4f9c6eba122ec5207fa21de4d78a")
        self.DB_URL = os.getenv("DATABASE_URL", "sqlite:///./partners.db")
        self.MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4")
        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
        self.CRAWLER_TIMEOUT = int(os.getenv("CRAWLER_TIMEOUT", 15))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
print(settings)
