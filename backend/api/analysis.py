from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from core.engine import MarketEngine
from core.patterns import PatternRecognition
from core.ai_interpreter import AIInterpreter
from core.risk import RiskEngine

router = APIRouter()

# -----------------------------
# CORE SYSTEMS
# -----------------------------

market_engine = MarketEngine()
pattern_engine = PatternRecognition()
ai = AIInterpreter()
risk_engine = RiskEngine()


# -----------------------------
# REQUEST MODEL
# -----------------------------

class AnalysisRequest(BaseModel):
    prices: List[float]


# -----------------------------
# MAIN ANALYSIS ENDPOINT
# -----------------------------

@router.post("/analysis/run")
def run_analysis(request: AnalysisRequest):
    """
    Full A.I.M intelligence analysis pipeline.

    Combines:
    - Market structure
    - Pattern detection
    - AI interpretation
    - Risk scoring
    """

    prices = request.prices

    if not prices or len(prices) < 5:
        return {
            "error": "Insufficient data",
            "message": "At least 5 price points required for analysis"
        }

    # -----------------------------
    # 1. MARKET ENGINE
    # -----------------------------
    market_signal = market_engine.ingest_market_data(prices)

    # -----------------------------
    # 2. PATTERN DETECTION
    # -----------------------------
    patterns = pattern_engine.detect(prices)

    # -----------------------------
    # 3. AI INTERPRETATION
    # -----------------------------
    explanation = ai.explain(market_signal)

    # -----------------------------
    # 4. RISK ANALYSIS
    # -----------------------------
    risk = risk_engine.analyze(prices)

    # -----------------------------
    # FINAL STRUCTURED OUTPUT
    # -----------------------------
    return {
        "status": "success",
        "input_size": len(prices),

        "market": {
            "trend_strength": market_signal.get("trend_strength"),
            "volatility": market_signal.get("volatility"),
            "signal": market_signal.get("signal")
        },

        "patterns": patterns,

        "ai_insight": {
            "summary": explanation.get("summary"),
            "risk_level": explanation.get("risk_level"),
            "confidence": explanation.get("confidence")
        },

        "risk": {
            "level": risk.risk_level,
            "score": risk.risk_score,
            "volatility": risk.volatility,
            "drawdown": risk.drawdown_risk,
            "recommendation": risk.recommendation
        }
    }


# -----------------------------
# SIMPLIFIED ANALYSIS (BEGINNER MODE)
# -----------------------------

@router.post("/analysis/simple")
def simple_analysis(request: AnalysisRequest):
    """
    Beginner-friendly output (plain language only)
    """

    prices = request.prices

    market_signal = market_engine.ingest_market_data(prices)
    risk = risk_engine.analyze(prices)

    direction = market_signal.get("signal")

    return {
        "market_direction": direction,
        "message": (
            "Market is trending upward" if direction == "BUY"
            else "Market is trending downward"
        ),
        "risk_level": risk.risk_level,
        "recommendation": risk.recommendation
    }


# -----------------------------
# DEBUG ENDPOINT (DEVELOPER ONLY)
# -----------------------------

@router.post("/analysis/debug")
def debug_analysis(request: AnalysisRequest):
    """
    Raw system outputs for debugging / model tuning
    """

    prices = request.prices

    return {
        "raw_prices": prices,
        "market_engine": market_engine.ingest_market_data(prices),
        "patterns": pattern_engine.detect(prices),
        "risk_raw": risk_engine.analyze(prices).__dict__
    }
