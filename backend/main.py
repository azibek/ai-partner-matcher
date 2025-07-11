from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from backend.agents.matcher_agent import generate_matches
from backend.schemas import PartnerMatch, ProductInput
from backend.db.init_db import init_db
from backend.db.models import Company
from backend.schemas import DiscoveryInput
from backend.agents.pipeline import run_discovery_pipeline
import traceback
from contextlib import asynccontextmanager



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




@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Setup tables and DB on startup
    yield
    # (Optional) Cleanup actions go here

app = FastAPI(lifespan=lifespan)

# Allow CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/discover")
async def discover_partners(payload: DiscoveryInput):
    try:
        companies = await run_discovery_pipeline(payload.product_description)
        return [c.as_dict() for c in companies]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))