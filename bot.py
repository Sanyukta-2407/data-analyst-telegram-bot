import json
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PUBLIC_LOG_URL = os.getenv("PUBLIC_LOG_URL", "")

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)


def append_log(entry):
    with open("run.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    append_log({
        "time": datetime.utcnow().isoformat(),
        "role": "user",
        "content": user_message
    })

    prompt = f"""
You are a data analyst.

Answer the user's question.

Return ONLY the answer.
Question:
{user_message}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert data analyst."},
            {"role": "user", "content": prompt},
        ],
    )

    answer = response.choices[0].message.content.strip()

    append_log({
        "time": datetime.utcnow().isoformat(),
        "role": "assistant",
        "content": answer
    })

    result = {
        "answer": answer,
        "log_url": PUBLIC_LOG_URL
    }

    await update.message.reply_text(json.dumps(result))


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()