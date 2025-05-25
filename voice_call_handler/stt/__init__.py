from flask import Blueprint

stt_bp = Blueprint('stt', __name__, url_prefix='/api/v1/stt')

# Импортируем маршруты, чтобы они регистрировались при инициализации
from . import stt  # noqa: F401 