import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from voice_call_handler.dialog import handle_dialog

def test_room_cleaning():
    text = "Пожалуйста, уберите в номере 305 сегодня вечером."
    response = handle_dialog(text)
    assert "Уборка будет организована" in response

def test_late_checkout():
    text = "Можно ли выехать чуть позже завтра?"
    response = handle_dialog(text)
    assert "Поздний выезд возможен" in response

def test_room_booking():
    text = "Здравствуйте, я хочу забронировать номер с 5 по 7 июня на двоих."
    response = handle_dialog(text)
    assert "помогу вам с бронированием" in response

def test_food_order():
    text = "Можно мне ужин в номер 217 в 8 вечера?"
    response = handle_dialog(text)
    assert "Что вы хотите заказать" in response

def test_wake_up_call():
    text = "Разбудите меня в 6 утра, пожалуйста."
    response = handle_dialog(text)
    assert "wake-up call" in response

def test_complaint():
    text = "В комнате шумно и очень грязно, уберите пожалуйста."
    response = handle_dialog(text)
    assert "извинения за неудобства" in response

def test_unknown():
    text = "А можно фиолетовый дракон?"
    response = handle_dialog(text)
    assert "Извините, я не совсем понял" in response 