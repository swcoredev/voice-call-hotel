from flask import Blueprint, request, jsonify
from .logic import analyze_text
from .schemas import TextIn, AnalyzeOut
import os
from sqlalchemy import create_engine

lang_bp = Blueprint('lang', __name__, url_prefix='/api/v1/lang')

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'voice_hotel_db')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'adminvoice')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'SecurePass123')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

@lang_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400
    text_in = TextIn(**data)
    result = analyze_text(text_in.text)
    return jsonify(AnalyzeOut(**result).dict()) 