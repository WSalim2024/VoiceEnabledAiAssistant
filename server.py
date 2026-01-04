import base64
import json
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from worker import speech_to_text, text_to_speech, watsonx_process_message

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("Processing Speech-to-Text")
    audio_binary = request.data
    text = speech_to_text(audio_binary)

    # Return JSON response
    return jsonify({'text': text})


@app.route('/process-message', methods=['POST'])
def process_message_route():
    data = request.json
    user_message = data.get('userMessage', '')
    voice = data.get('voice', 'default')

    print(f"User Message: {user_message}")
    print(f"Selected Voice: {voice}")

    # 1. Get Text Response from LLM
    response_text = watsonx_process_message(user_message)

    # Clean empty lines
    response_text = os.linesep.join([s for s in response_text.splitlines() if s])

    # 2. Convert Response to Audio
    audio_content = text_to_speech(response_text, voice)

    # 3. Encode audio to base64 for the browser
    response_speech_b64 = base64.b64encode(audio_content).decode('utf-8')

    # 4. Send back to frontend
    return jsonify({
        "watsonxResponseText": response_text,
        "watsonxResponseSpeech": response_speech_b64
    })


if __name__ == "__main__":
    # Windows-friendly port
    app.run(port=8000, debug=True)