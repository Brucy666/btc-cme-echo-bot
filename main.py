# main.py

from fastapi import FastAPI, Request
import uvicorn
from alert_parser import parse_alert
from reversal_scorer import score_reversal_signal
from discord_alerts import send_discord_echo_alert

app = FastAPI()

@app.post("/cme")
async def handle_cme_alert(request: Request):
    try:
        payload = await request.json()
        alert_message = payload.get("alert") or str(payload)
        print("[ALERT RECEIVED]", alert_message)

        parsed = parse_alert(alert_message)
        if not parsed:
            print("[!] Unrecognized alert format.")
            return {"status": "ignored"}

        scored = score_reversal_signal(parsed)
        await send_discord_echo_alert(parsed, scored)

        return {"status": "ok", "score": scored}

    except Exception as e:
        print("[ERROR] Echo Engine:", e)
        return {"status": "error", "message": str(e)}


@app.get("/")
async def root():
    return {"status": "btc-cme-echo-bot live"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
