from .logic import analyze_text

def test_booking():
    assert analyze_text('Хочу забронировать номер')['intent'] == 'booking'
    assert analyze_text('Please book a room')['intent'] == 'booking'

def test_cancel():
    assert analyze_text('Отмена брони')['intent'] == 'cancel'
    assert analyze_text('cancel reservation')['intent'] == 'cancel'

def test_info():
    assert analyze_text('Инфо по отелю')['intent'] == 'info'
    assert analyze_text('I want info')['intent'] == 'info'

def test_unknown():
    assert analyze_text('Привет')['intent'] == 'unknown' 