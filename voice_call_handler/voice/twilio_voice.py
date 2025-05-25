from flask import request, Response, jsonify
from twilio.twiml.voice_response import VoiceResponse

# Все маршруты и app вынесены в Blueprint voice_bp в __init__.py
# Этот файл можно оставить пустым или использовать для вспомогательных функций, если потребуется.
