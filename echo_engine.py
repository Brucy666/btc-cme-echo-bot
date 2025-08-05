# echo_engine.py

import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from alert_parser import parse_alert
from reversal_scorer import score_reversal_signal
from discord_alerts import send_discord_echo_alert
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/echo-alert")
async def handle_echo_alert(request: Request):
    try:
        body = await request.json()
        alert_text = body.get("alert", "")

        parsed = parse_alert(alert_text)
        if not parsed:
            return JSONResponse({"error": "Unrecognized alert format."}, status_code=400)

        scored = score_reversal_signal(parsed)
        await send_discord_echo_alert(parsed, scored)

        return JSONResponse({"status": "ok", "parsed": parsed, "scored": scored})

    except Exception as e:
        print("[ERROR] Echo Engine:", e)
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/")
async def root():
    return {"status": "echo bot online"}
