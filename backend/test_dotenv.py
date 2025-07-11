# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()
print("SERP_API_KEY:", os.getenv("SERP_API_KEY"))
