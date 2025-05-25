from flask import Blueprint, request, Response, jsonify
from twilio.twiml.voice_response import VoiceResponse

voice_bp = Blueprint('voice_bp', __name__)

@voice_bp.before_request
def log_request():
    print(f"[LOG] {request.method} {request.path} from {request.remote_addr}")

@voice_bp.route("/voice", methods=["GET"])
def voice_status():
    return jsonify({"message": "VoiceCall Hotel API is running"})

@voice_bp.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.say("Здравствуйте! Чем могу помочь?", language="ru-RU", voice="Polly.Tatyana")
    return Response(str(response), mimetype="text/xml")

@voice_bp.route("/", methods=["GET"])
def root():
    return jsonify({"message": "VoiceCall Hotel API is running"}) 