from voice_call_handler.lang.logic import detect_intent

def handle_dialog(text: str) -> str:
    result = detect_intent(text)
    intent = result.get("intent")
    if intent == "room_cleaning":
        return "Уборка будет организована в ближайшее время. Спасибо!"
    elif intent == "late_checkout":
        return "Поздний выезд возможен при наличии свободных номеров. Я уточню и сообщу."
    elif intent == "room_booking":
        return "Конечно! Я помогу вам с бронированием. Уточните, пожалуйста, даты и количество гостей."
    elif intent == "food_order":
        return "С удовольствием! Что вы хотите заказать и на какое время?"
    elif intent == "wake_up_call":
        return "Я установлю wake-up call на указанное время. Хорошего отдыха!"
    elif intent == "complaint":
        return "Приносим извинения за неудобства. Я передам это ответственному сотруднику."
    else:
        return "Извините, я не совсем понял. Повторите, пожалуйста." 