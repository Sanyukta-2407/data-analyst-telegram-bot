import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://aipipe.org/openrouter/v1"
)

try:
    models = client.models.list()
    for m in models.data:
        print(m.id)
except Exception as e:
    print(e)