from flask import Flask, request, jsonify
import whisper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
CORS(app, supports_credentials=True, allow_headers=['Form-data', 'Authorization'], methods=['GET', 'POST', 'OPTIONS'])

# Initialize the Whisper model
model = whisper.load_model("base")

@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    # Check if the request has an audio file
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    
    # You might need to save the file temporarily or directly pass the file stream
    audio_path = './temp_audio.wav'
    audio_file.save(audio_path)

    # Transcribe the audio
    result = model.transcribe(audio_path)
    
    # Cleanup the temporary file if needed
    # os.remove(audio_path)

    # Return the transcription
    return jsonify({'transcription': result['text']})

if __name__ == "__main__":
    app.run(debug=True,port=5002)
