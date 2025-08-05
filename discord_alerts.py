# discord_alerts.py

import os
import httpx
import asyncio

WEBHOOK_URL = os.getenv("DISCORD_ECHO_WEBHOOK")

async def send_discord_echo_alert(parsed, scored):
    if not WEBHOOK_URL:
        print("[X] DISCORD_ECHO_WEBHOOK not set in .env")
        return

    direction_icon = "🟢 LONG" if scored["bias"] == "long" else "🔴 SHORT" if scored["bias"] == "short" else "⚪ NEUTRAL"

    reasons = "\n".join(f"• {r}" for r in scored["reasons"])

    embed = {
        "title": "💥 Brucy Echo Reversal Alert",
        "description": f"{direction_icon}\n\n**Confidence:** `{scored['score']}/10`\n**Timeframe:** `{parsed['timeframe']}`\n\n**Reasons:**\n{reasons}",
        "color": 15158332 if scored["bias"] == "short" else 3066993 if scored["bias"] == "long" else 8421504
    }

    payload = {
        "username": "Echo Bot",
        "embeds": [embed]
    }

    try:
        async with httpx.AsyncClient() as client:
            await client.post(WEBHOOK_URL, json=payload)
        print("[✓] Echo alert sent to Discord.")
    except Exception as e:
        print("[X] Failed to send echo alert:", e)
