def analyze_market(prices):
    # WAIT UNTIL ENOUGH PRICE SAMPLES ARE COLLECTED
    if len(prices) < 20:
        return 0, "waiting", None

    # CALCULATE MARKET VOLATILITY
    price_min = min(prices)
    price_max = max(prices)
    price_now = prices[-1]

    volatility = ((price_max - price_min) / price_now) * 100
    force = None

    # CLASSIFY MARKET TYPE
    if volatility < 0.5:
        market_type = "LATERAL"

    elif volatility > 1.5:
        slope = ((prices[-1] - prices[0]) / prices[0]) * 100

        # ESTIMATE TREND STRENGTH
        force = (
            "WEAK" if abs(slope) < 0.3 else "MEDIUM" if abs(slope) < 0.7 else "STRONG"
        )

        if prices[-1] > prices[0]:
            market_type = "VOLATILE-UPTREND"
        else:
            market_type = "VOLATILE-DOWNREND"

    else:
        market_type = "MODERATE"

    return volatility, market_type, force
