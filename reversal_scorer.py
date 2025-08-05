# reversal_scorer.py

def score_reversal_signal(parsed):
    """
    Input: parsed dict from alert_parser
    Output: dict with confidence score and bias
    """
    score = 0
    bias = "neutral"
    reasons = []

    # --- RSI Contribution ---
    if parsed["rsi"] == "overbought":
        score += 4
        bias = "short"
        reasons.append("RSI overbought")
    elif parsed["rsi"] == "oversold":
        score += 4
        bias = "long"
        reasons.append("RSI oversold")
    elif parsed["rsi"] == "breakdown":
        score += 2
        bias = "short"
        reasons.append("RSI breakdown")
    elif parsed["rsi"] == "reclaim":
        score += 2
        bias = "long"
        reasons.append("RSI reclaim")

    # --- VWAP Contribution ---
    if parsed["vwap"] == "reject":
        score += 3
        if bias == "long":
            score -= 2  # conflicting
        else:
            bias = "short"
        reasons.append("VWAP rejection")
    elif parsed["vwap"] == "reclaim":
        score += 3
        if bias == "short":
            score -= 2
        else:
            bias = "long"
        reasons.append("VWAP reclaim")
    elif parsed["vwap"] == "cross_up":
        score += 1
        bias = "long"
        reasons.append("VWAP cross up")
    elif parsed["vwap"] == "cross_down":
        score += 1
        bias = "short"
        reasons.append("VWAP cross down")

    # --- Divergence Contribution ---
    if parsed["divergence"] == "hidden_bull":
        score += 2
        bias = "long"
        reasons.append("Hidden bullish divergence")
    elif parsed["divergence"] == "hidden_bear":
        score += 2
        bias = "short"
        reasons.append("Hidden bearish divergence")

    # Clamp and normalize
    score = max(0, min(score, 10))

    return {
        "score": round(score, 2),
        "bias": bias,
        "reasons": reasons
    }
