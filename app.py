from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
import os
from dotenv import load_dotenv
from memory import add_message, get_history

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
        chat_id = update.message.chat.id
        user_text = update.message.text

    # Save the user's message
        add_message(chat_id, "user", user_text)

    # Get the conversation history
        history = get_history(chat_id)

    # Temporary reply showing how many messages we've stored
        reply = f"I have stored {len(history)} message(s)."

    # Save the assistant's reply
        add_message(chat_id, "assistant", reply)

        await telegram_app.bot.send_message(
            chat_id=chat_id,
            text=reply
       )