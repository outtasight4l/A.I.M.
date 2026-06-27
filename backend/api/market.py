from fastapi import APIRouter
from core.engine import MarketEngine

router = APIRouter()
engine = MarketEngine()

@router.get("/market/analyze")
def analyze(price_data: list):
    return engine.ingest_market_data(price_data)