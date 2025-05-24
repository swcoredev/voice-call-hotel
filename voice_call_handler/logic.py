def handle_voice_text(text: str) -> str:
    text = text.lower()

    if "номер" in text and "забронировать" in text:
        return "Вы хотите забронировать номер. Назовите, пожалуйста, даты проживания."
    elif "заселение" in text:
        return "Заселение возможно с 14:00."
    elif "люкс" in text:
        return "Номера класса 'люкс' доступны. Хотите забронировать?"
    else:
        return "Извините, я не понял запрос. Повторите, пожалуйста."
