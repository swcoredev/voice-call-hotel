import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from voice_call_handler.lang.logic import detect_intent

def test_room_cleaning():
    result = detect_intent("Пожалуйста, уберите в номере 305 сегодня вечером.")
    print("\n[room_cleaning]", result)
    assert result["intent"] == "room_cleaning"
    assert str(result["room_number"]) == "305" or result["room_number"] is None
    assert result["confidence"] > 0.5

def test_food_order():
    text = "Я бы хотел заказать ужин в номер 305 через час."
    result = detect_intent(text)
    print("\nЗаказ еды:", result)

def test_late_checkout():
    result = detect_intent("Можно ли выехать чуть позже завтра?")
    print("\n[late_checkout]", result)
    assert result["intent"] == "late_checkout"
    assert result["confidence"] > 0.5

def test_room_booking():
    result = detect_intent("Я хочу забронировать номер на двоих с 5 по 7 июня.")
    assert result["intent"] == "room_booking"
    assert result["confidence"] > 0.5

def test_food_order():
    result = detect_intent("Можно мне ужин в номер 217 в 8 вечера?")
    assert result["intent"] == "food_order"
    assert result["confidence"] > 0.5
    # Проверяем наличие времени, если модель его извлекла
    assert result["time"] is None or isinstance(result["time"], str)

def test_wake_up_call():
    result = detect_intent("Разбудите меня в 6 утра, пожалуйста.")
    assert result["intent"] == "wake_up_call"
    assert result["confidence"] > 0.5
    assert result["time"] is None or isinstance(result["time"], str)

def test_complaint():
    result = detect_intent("В комнате шумно и очень грязно, уберите пожалуйста.")
    assert result["intent"] == "complaint"
    assert result["confidence"] > 0.5

def test_unknown_intent():
    result = detect_intent("А можно фиолетовый дракон?")
    print("\n[unknown]", result)
    assert result["intent"] == "unknown"

def test_unknown():
    text = "У вас такой приятный запах в холле!"
    result = detect_intent(text)
    print("\nНепонятный текст:", result) 