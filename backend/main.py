from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from backend.agents.matcher_agent import generate_matches
from backend.schemas import PartnerMatch, ProductInput
import traceback
app = FastAPI(title="AI Partner Matcher")

# CORS for local dev (adjust in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======== Request & Response Schemas ========


# ======== API Route ========
@app.post("/match", response_model=List[PartnerMatch])
async def match_partners(input: ProductInput):
    try:
        matches = await generate_matches(input.product_description)
        return matches
    except Exception as e:
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))
