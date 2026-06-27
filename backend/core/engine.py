import numpy as np

class MarketEngine:
    def __init__(self):
        self.memory = []

    def ingest_market_data(self, data):
        self.memory.append(data)
        return self._process(data)

    def _process(self, data):
        trend = np.mean(data[-20:])
        volatility = np.std(data[-20:])

        return {
            "trend_strength": float(trend),
            "volatility": float(volatility),
            "signal": "BUY" if trend > 0 else "SELL"
        }