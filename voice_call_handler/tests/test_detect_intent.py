import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from voice_call_handler.lang.logic import detect_intent

def test_room_cleaning():
    result = detect_intent("Пожалуйста, уберите в номере 305 сегодня вечером.")
    print("\n[room_cleaning]", result)
    assert result["intent"] == "room_cleaning"
    assert str(result["room_number"]) == "305"
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

def test_unknown_intent():
    result = detect_intent("А можно фиолетовый дракон?")
    print("\n[unknown]", result)
    assert result["intent"] == "unknown"

def test_unknown():
    text = "У вас такой приятный запах в холле!"
    result = detect_intent(text)
    print("\nНепонятный текст:", result) 