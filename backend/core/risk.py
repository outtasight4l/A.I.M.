import numpy as np
from dataclasses import dataclass

@dataclass
class RiskProfile:
    risk_level: str
    risk_score: float
    volatility: float
    drawdown_risk: float
    recommendation: str


class RiskEngine:
    """
    Institutional-style risk analysis engine for A.I.M.
    Converts raw market signals into structured risk intelligence.
    """

    def __init__(self):
        self.volatility_window = 20
        self.high_risk_threshold = 0.75
        self.medium_risk_threshold = 0.40

    def calculate_volatility(self, prices):
        if len(prices) < 2:
            return 0.0
        return float(np.std(prices[-self.volatility_window:]))

    def calculate_drawdown_risk(self, prices):
        if len(prices) < 2:
            return 0.0

        peak = max(prices)
        current = prices[-1]

        drawdown = (peak - current) / peak if peak != 0 else 0
        return float(drawdown)

    def compute_risk_score(self, volatility, drawdown_risk):
        """
        Weighted risk formula (can be tuned later with ML)
        """
        score = (volatility * 0.6) + (drawdown_risk * 0.4)

        # normalize to 0–1 range
        return float(min(max(score, 0.0), 1.0))

    def classify_risk(self, score):
        if score >= self.high_risk_threshold:
            return "HIGH"
        elif score >= self.medium_risk_threshold:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_recommendation(self, risk_level):
        if risk_level == "HIGH":
            return "Reduce exposure / avoid new positions"
        elif risk_level == "MEDIUM":
            return "Trade cautiously with tight risk management"
        else:
            return "Favorable conditions for structured entries"

    def analyze(self, prices):
        """
        Main entry point
        """

        volatility = self.calculate_volatility(prices)
        drawdown = self.calculate_drawdown_risk(prices)

        risk_score = self.compute_risk_score(volatility, drawdown)
        risk_level = self.classify_risk(risk_score)
        recommendation = self.generate_recommendation(risk_level)

        return RiskProfile(
            risk_level=risk_level,
            risk_score=risk_score,
            volatility=volatility,
            drawdown_risk=drawdown,
            recommendation=recommendation
        )
