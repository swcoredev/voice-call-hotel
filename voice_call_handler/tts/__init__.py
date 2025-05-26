from flask import Blueprint, request, jsonify, send_file
from .tts import speak_text
from .schemas import TTSText
from dotenv import load_dotenv

load_dotenv()

tts_bp = Blueprint('tts', __name__, url_prefix='/api/v1/tts')

@tts_bp.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400
    tts_in = TTSText(**data)
    result = speak_text(tts_in.text)
    return jsonify(result)

@tts_bp.route("/welcome", methods=["GET"])
def play_welcome_message():
    return send_file("static/ElevenLabs_Untitled_Project.wav", mimetype="audio/wav") 