import io
from pydub import AudioSegment
import requests
import speech_recognition as sr
import edge_tts
import asyncio
import os

# --- FFmpeg Configuration (The "Nuclear Option") ---
# We force pydub to look for ffmpeg.exe and ffprobe.exe in the CURRENT folder.
# This fixes the "FileNotFound" or "WinError 2" issues on Windows.

script_dir = os.path.dirname(os.path.abspath(__file__))

# Explicitly set the paths
AudioSegment.converter = os.path.join(script_dir, "ffmpeg.exe")
AudioSegment.ffmpeg = os.path.join(script_dir, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(script_dir, "ffprobe.exe")


# ---------------------------------------------------

# 1. THE BRAIN: OLLAMA (Local LLM)
# We keep the function name 'watsonx_process_message' so server.py doesn't break.
def watsonx_process_message(user_message):
    # Endpoint for your local Ollama instance
    url = "http://localhost:11434/api/generate"

    # Prompt engineering: We tell it to be a helpful voice assistant.
    prompt = f"You are a helpful, concise voice assistant. Answer this query naturally: {user_message}"

    payload = {
        "model": "mistral",  # Ensure you ran 'ollama run mistral' in cmd
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        # Extract the actual text from Ollama's JSON response
        response_text = response.json().get('response', '')
        print(f"Ollama response: {response_text}")
        return response_text.strip()
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return "I'm having trouble thinking right now. Please check if Ollama is running."


# 2. THE EARS: Speech Recognition (With FFmpeg Conversion)
def speech_to_text(audio_binary):
    recognizer = sr.Recognizer()

    try:
        print("Received audio, attempting conversion...")

        # A. Convert WebM (Browser format) -> WAV (Python format)
        # We read the binary data using BytesIO
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_binary))

        # Export as .wav to a memory buffer so we don't need a temp file on disk
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)  # Reset pointer to start of file

        # B. Process the WAV data
        with sr.AudioFile(wav_io) as source:
            # Listen to the data
            audio_data = recognizer.record(source)

            # Send to Google for transcription (Free API)
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text}")
            return text

    except sr.UnknownValueError:
        print("STT: Could not understand audio")
        return "I didn't catch that."
    except sr.RequestError as e:
        print(f"STT Connection Error: {e}")
        return "I can't reach the speech service."
    except Exception as e:
        # This prints the actual system error to your terminal for debugging
        print(f"CRITICAL STT ERROR: {e}")
        return "I am having trouble processing your voice."


# 3. THE VOICE: Edge TTS (Free Neural Voice)
# Internal async function that does the heavy lifting
async def _generate_audio(text, voice):
    # Mapping simple voice names to Edge-TTS locales
    voice_map = {
        "default": "en-US-AriaNeural",
        "Laura (Castilian Spanish)": "es-ES-ElviraNeural",
        "en-US_AllisonV3Voice": "en-US-AriaNeural",
        "es-US_SofiaV3Voice": "es-ES-ElviraNeural"
    }

    selected_voice = voice_map.get(voice, "en-US-AriaNeural")
    communicate = edge_tts.Communicate(text, selected_voice)

    # EdgeTTS requires saving to a file first
    output_file = "output_voice.mp3"
    await communicate.save(output_file)

    # Read the file back into memory
    with open(output_file, "rb") as f:
        audio_content = f.read()

    return audio_content


# Wrapper to run the async function synchronously (called by server.py)
def text_to_speech(text, voice=""):
    return asyncio.run(_generate_audio(text, voice))