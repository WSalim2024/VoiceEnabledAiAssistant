# Voice Enabled AI Assistant (Local & Free)

This project is a privacy-focused, voice-enabled AI assistant that runs locally on your machine. It replaces proprietary cloud services (like IBM Watson) with powerful free and open-source alternatives.

## 🏗 Architecture

We swapped the "Engine" parts for free, high-quality alternatives:

* **The Brain (LLM):** [Ollama](https://ollama.com/) (Running Mistral or Llama 3 locally).
* **The Ears (STT):** `SpeechRecognition` library (using Google's free Web API) + `FFmpeg` for audio conversion.
* **The Voice (TTS):** `Edge-TTS` (Uses Microsoft Edge's free online neural voices).
* **The Backend:** Python Flask.
* **The Frontend:** HTML/JS/Bootstrap (Classic chat interface).

## 🚀 Prerequisites

Before running the app, ensure you have the following installed:

1.  **Python 3.10+**
2.  **Ollama** (for the AI Brain):
    * Download from [ollama.com](https://ollama.com).
    * Run `ollama run mistral` in your terminal to download the model.

## 🛠 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/WSalim2024/VoiceEnabledAiAssistant.git](https://github.com/WSalim2024/VoiceEnabledAiAssistant.git)
    cd VoiceEnabledAiAssistant
    ```

2.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **setup Audio Engine (FFmpeg):**
    * *Note: Due to file size limits, the audio engine is not included in this repo.*
    * Download the "Essentials Build" from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip).
    * Extract the ZIP file.
    * Copy `ffmpeg.exe` and `ffprobe.exe` from the `bin` folder.
    * **Paste them directly into this project's root folder** (next to `server.py`).

## ▶️ Usage

1.  **Start Ollama** (if not already running):
    * Open a terminal and ensure `ollama run mistral` is active or the service is running in the background.

2.  **Start the Server:**
    ```bash
    python server.py
    ```

3.  **Open the Interface:**
    * Go to `http://127.0.0.1:8000` in your browser.
    * Click the microphone icon and speak. The AI will listen, think, and reply with voice.

## 📂 Project Structure

* `server.py`: The Flask backend controller.
* `worker.py`: Handles the heavy lifting (talking to Ollama, converting audio, generating speech).
* `static/`: CSS and JavaScript files.
* `templates/`: HTML interface.

## 📝 Notes for Windows Users

This project uses a "portable" FFmpeg setup. The code in `worker.py` is hardcoded to look for `ffmpeg.exe` in the current folder to avoid System PATH issues common on Windows.