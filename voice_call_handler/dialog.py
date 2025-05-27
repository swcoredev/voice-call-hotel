from voice_call_handler.lang.logic import detect_intent

def handle_dialog(text: str) -> str:
    result = detect_intent(text)
    intent = result.get("intent")
    room_number = result.get("room_number")
    time = result.get("time")
    if intent == "room_cleaning":
        room = f"{room_number}" if room_number else "указанном номере"
        time_str = f" {time}" if time else ""
        return f"Уборка будет выполнена в номере {room}{time_str}."
    elif intent == "late_checkout":
        return "Поздний выезд возможен. Я отмечу это в системе."
    elif intent == "room_booking":
        return "Конечно! Я помогу вам с бронированием. Уточните, пожалуйста, даты и количество гостей."
    else:
        return "Извините, я не совсем понял. Повторите, пожалуйста." 