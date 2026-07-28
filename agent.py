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

Return exactly what the user requests.
If the user asks for JSON, return only JSON.
"""

def ask_llm(messages):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            *messages
        ]
    )

    return response.choices[0].message.content