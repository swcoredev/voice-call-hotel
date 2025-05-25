from flask import Flask, request, jsonify, render_template_string
from voice_call_handler.stt import stt_bp
from voice_call_handler.logic import handle_voice_text

app = Flask(__name__)
app.register_blueprint(stt_bp)

@app.route("/api/v1/voice/process", methods=["POST"])
def process_voice():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400
    response = handle_voice_text(data["text"])
    return jsonify({"response": response})

@app.route("/upload", methods=["GET"])
def upload_form():
    return render_template_string('''
        <!doctype html>
        <title>Upload audio for STT</title>
        <h1>Upload audio file for STT</h1>
        <form id="uploadForm" enctype="multipart/form-data">
          <input type="file" name="audio" accept="audio/*" required>
          <input type="submit" value="Upload">
        </form>
        <div id="result" style="margin-top:1em;"></div>
        <script>
        document.getElementById('uploadForm').onsubmit = async function(e) {
          e.preventDefault();
          const form = e.target;
          const data = new FormData(form);
          document.getElementById('result').innerText = 'Загрузка...';
          const resp = await fetch('/api/v1/stt/process', {
            method: 'POST',
            body: data
          });
          let msg = '';
          try {
            const json = await resp.json();
            if (json.text) {
              msg = json.text;
            } else if (json.error) {
              msg = 'Ошибка: ' + json.error;
            } else {
              msg = 'Неизвестный ответ';
            }
          } catch {
            msg = 'Ошибка обработки ответа';
          }
          document.getElementById('result').innerText = msg;
        };
        </script>
    ''')

@app.route("/")
def index():
    return "VoiceCall Hotel API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
