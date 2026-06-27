class AIInterpreter:
    def explain(self, market_signal):
        return {
            "summary": f"Market shows {market_signal['signal']} bias",
            "risk_level": "HIGH" if abs(market_signal["volatility"]) > 1 else "MEDIUM",
            "confidence": min(0.95, abs(market_signal["trend_strength"]))
        }