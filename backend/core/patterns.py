class PatternRecognition:
    def detect(self, candles):
        patterns = []

        if len(candles) < 5:
            return []

        if candles[-1] > candles[-2] > candles[-3]:
            patterns.append("bullish_continuation")

        if candles[-1] < candles[-2] < candles[-3]:
            patterns.append("bearish_continuation")

        return patterns