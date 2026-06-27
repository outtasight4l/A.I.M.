from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from core.engine import MarketEngine
from core.patterns import PatternRecognition
from core.ai_interpreter import AIInterpreter
from core.risk import RiskEngine

router = APIRouter()

# Initialize core systems
market_engine = MarketEngine()
pattern_engine = PatternRecognition()
ai = AIInterpreter()
risk_engine = RiskEngine()


# -----------------------------
# REQUEST MODELS
# -----------------------------

class MarketRequest(BaseModel):
    prices: List[float]


# -----------------------------
# HEALTH CHECK
# -----------------------------

@router.get("/health")
def health():
    return {
        "status": "online",
        "system": "A.I.M Asset Intelligence Matrix",
        "mode": "analysis engine active"
    }


# -----------------------------
# MARKET ANALYSIS PIPELINE
# -----------------------------

@router.post("/analyze/full")
def full_analysis(request: MarketRequest):
    """
    Runs full institutional analysis pipeline:
    Market → Patterns → AI Interpretation → Risk Engine
    """

    prices = request.prices

    # 1. Market Engine Signal
    market_signal = market_engine.ingest_market_data(prices)

    # 2. Pattern Detection
    patterns = pattern_engine.detect(prices)

    # 3. AI Interpretation
    explanation = ai.explain(market_signal)

    # 4. Risk Analysis
    risk = risk_engine.analyze(prices)

    return {
        "market_signal": market_signal,
        "patterns": patterns,
        "ai_explanation": explanation,
        "risk": {
            "level": risk.risk_level,
            "score": risk.risk_score,
            "volatility": risk.volatility,
            "drawdown_risk": risk.drawdown_risk,
            "recommendation": risk.recommendation
        }
    }


# -----------------------------
# LIGHTWEIGHT ENDPOINTS
# -----------------------------

@router.post("/analyze/market")
def market_only(request: MarketRequest):
    return market_engine.ingest_market_data(request.prices)


@router.post("/analyze/patterns")
def pattern_only(request: MarketRequest):
    return pattern_engine.detect(request.prices)


@router.post("/analyze/risk")
def risk_only(request: MarketRequest):
    r = risk_engine.analyze(request.prices)

    return {
        "risk_level": r.risk_level,
        "risk_score": r.risk_score,
        "recommendation": r.recommendation
    }


# -----------------------------
# AI EXPLANATION ONLY
# -----------------------------

@router.post("/analyze/explain")
def explain_only(request: MarketRequest):
    market_signal = market_engine.ingest_market_data(request.prices)
    return ai.explain(market_signal)


# -----------------------------
# HISTORY PLACEHOLDER
# -----------------------------

@router.get("/history")
def history():
    """
    Placeholder for activity center / history menu
    (connect to DB later)
    """
    return [
        "System initialized",
        "Market engine active",
        "Risk engine running",
        "AI interpreter online"
    ]
