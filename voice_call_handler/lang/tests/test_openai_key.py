import os
import openai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY не найден в .env файле")
    exit(1)

openai.api_key = api_key

try:
    models = openai.models.list()
    print("✅ Ключ работает! Получены модели OpenAI:")
    for model in models.data[:5]:
        print("-", model.id)
except Exception as e:
    print("❌ Ошибка при обращении к OpenAI:", e)
