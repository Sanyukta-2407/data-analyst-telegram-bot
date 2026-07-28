from fastapi import FastAPI, Request

app = FastAPI(title="Data Analyst Telegram Bot")


@app.get("/")
async def home():
    return {
        "status": "ok",
        "service": "telegram-data-analyst"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    print(data)  # We'll replace this later

    return {"ok": True}