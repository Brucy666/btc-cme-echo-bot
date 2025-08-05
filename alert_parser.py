# alert_parser.py

def parse_alert(text):
    """
    Parse a TradingView alert string into structured signal components.
    Expected input: freeform text like
        "CME BTC RSI > 80 + VWAP Reject 15m"
    """
    text = text.strip().lower()

    parsed = {
        "rsi": None,
        "vwap": None,
        "divergence": None,
        "timeframe": "15m",
        "raw": text
    }

    # --- RSI ---
    if "rsi > 80" in text or "rsi overbought" in text:
        parsed["rsi"] = "overbought"
    elif "rsi < 30" in text or "rsi oversold" in text:
        parsed["rsi"] = "oversold"
    elif "rsi breakdown" in text:
        parsed["rsi"] = "breakdown"
    elif "rsi reclaim" in text:
        parsed["rsi"] = "reclaim"

    # --- VWAP ---
    if "vwap reject" in text:
        parsed["vwap"] = "reject"
    elif "vwap reclaim" in text:
        parsed["vwap"] = "reclaim"
    elif "crossed above vwap" in text:
        parsed["vwap"] = "cross_up"
    elif "crossed below vwap" in text:
        parsed["vwap"] = "cross_down"

    # --- Hidden Divergence ---
    if "hidden bull div" in text:
        parsed["divergence"] = "hidden_bull"
    elif "hidden bear div" in text:
        parsed["divergence"] = "hidden_bear"

    # --- Timeframe ---
    for tf in ["1m", "3m", "5m", "15m", "30m", "1h"]:
        if tf in text:
            parsed["timeframe"] = tf

    # If nothing detected
    if not any([parsed["rsi"], parsed["vwap"], parsed["divergence"]]):
        return None

    return parsed
