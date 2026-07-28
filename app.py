from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = FastAPI(title="Data Analyst Telegram Bot")

telegram_app = Application.builder().token(BOT_TOKEN).build()


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
async def webhook(request: Request):
    data = await request.json()

    update = Update.de_json(data, telegram_app.bot)

    if update.message and update.message.text:
        await telegram_app.bot.send_message(
            chat_id=update.message.chat.id,
            text="Hello! Your bot is working."
        )

    return {"ok": True}