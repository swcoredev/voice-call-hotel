from flask import Blueprint, request, jsonify
from .tts import speak_text
from .schemas import TTSText

tts_bp = Blueprint('tts', __name__, url_prefix='/api/v1/tts')

@tts_bp.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400
    tts_in = TTSText(**data)
    # Здесь можно добавить сохранение в файл и отдачу файла, сейчас просто заглушка
    speak_text(tts_in.text)
    return jsonify({'result': 'Speech synthesized'}) 