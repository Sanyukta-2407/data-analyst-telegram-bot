import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://aipipe.org/openrouter/v1"
)

SYSTEM_PROMPT = """
You are an expert data analyst.

Rules:
1. Answer the user's question accurately.
2. If the user specifies a JSON format, return ONLY that JSON.
3. Do not include markdown.
4. Do not include explanations unless requested.
"""

def ask_llm(messages):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            *messages
        ]
    )

    return response.choices[0].message.content