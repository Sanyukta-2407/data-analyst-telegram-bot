from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
import os
from dotenv import load_dotenv
from memory import add_message, get_history
from fastapi.responses import FileResponse
from pathlib import Path
from agent import ask_llm
import json
from logger import log_event
load_dotenv()
print("API KEY FOUND:", bool(os.getenv("OPENAI_API_KEY")))
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

@app.get("/run.jsonl")
async def get_run_log():
    log_file = Path("run.jsonl")

    if not log_file.exists():
        log_file.write_text("", encoding="utf-8")

    return FileResponse(
        path=log_file,
        media_type="application/json",
        filename="run.jsonl"
    )
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    update = Update.de_json(data, telegram_app.bot)

    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_text = update.message.text

    # Save the user's message
        add_message(chat_id, "user", user_text)

    # Get the conversation history
        history = get_history(chat_id)
        log_event({
            "type": "user",
            "chat_id": chat_id,
            "message": user_text
        })
        reply = ask_llm(history)
        

        data = json.loads(reply)
        data["log_url"] = "https://data-analyst-telegram-bot-o1d5.onrender.com/run.jsonl"
        reply = json.dumps(data)
        add_message(chat_id, "assistant", reply)
        log_event({
            "type": "assistant",
            "chat_id": chat_id,
            "message": reply
        })
        await telegram_app.bot.send_message(
            chat_id=chat_id,
            text=reply
        )