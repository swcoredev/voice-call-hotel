def analyze_text(text: str):
    text_lower = text.lower()
    if any(word in text_lower for word in ['book', 'reserve', 'бронировать', 'заказать']):
        intent = 'booking'
    elif any(word in text_lower for word in ['cancel', 'отмена', 'отменить']):
        intent = 'cancel'
    elif any(word in text_lower for word in ['info', 'инфо', 'справка', 'узнать']):
        intent = 'info'
    else:
        intent = 'unknown'
    # entities можно расширить позже
    return {'intent': intent, 'entities': []} 