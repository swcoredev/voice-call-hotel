import os
from dotenv import load_dotenv
from loguru import logger

def check_env_variables():
    # Загружаем переменные окружения
    load_dotenv()
    
    # Список обязательных переменных
    required_vars = [
        "OPENAI_API_KEY",
        "ELEVENLABS_API_KEY",
        "ELEVENLABS_VOICE_ID",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD"
    ]
    
    # Проверяем каждую переменную
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value is None:
            missing_vars.append(var)
            logger.error(f"❌ {var} отсутствует в .env")
        else:
            # Маскируем значение для безопасности
            masked_value = value[:4] + "*" * (len(value) - 4) if len(value) > 4 else "****"
            logger.info(f"✅ {var} = {masked_value}")
    
    if missing_vars:
        logger.error(f"\nОтсутствуют следующие переменные: {', '.join(missing_vars)}")
        logger.error("Пожалуйста, добавьте их в файл .env")
    else:
        logger.success("\nВсе необходимые переменные окружения настроены правильно!")

if __name__ == "__main__":
    check_env_variables() 