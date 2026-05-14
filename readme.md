# 🇮🇳 Disha — The Hinglish Support AI
### Autonomous Multi-Agent Swarm for Indian Logistics

Western AIs don't understand our desi slang, and local uncles hate typing on apps. **Disha** is a voice-native, multi-agent swarm that listens to raw, angry Hinglish voice notes, understands the intent, securely queries a logistics database, and replies in a calming Indian voice. 

**Zero typing required.**

Built for the **Activate AI Hackathon** in under 10 hours using sovereign Indian AI models.

---

## ⚙️ Tech Stack
* **Speech-to-Text:** Sarvam Saaras v3 (Handles code-mixed Hinglish & phonetic Hindi tracking numbers)
* **LLM / Brain:** Sarvam-M (Free reasoning model)
* **Text-to-Speech:** Sarvam Bulbul v3 (Natural Indian voices)
* **Agentic Framework:** LangGraph (Multi-node routing and state management)
* **Backend:** FastAPI
* **Frontend:** Streamlit 

---

## 🏗️ System Architecture

1. **Voice-In:** User records a `.wav` file on the Streamlit frontend.
2. **Transcription:** FastAPI receives the audio and hits Saaras STT.
3. **LangGraph Swarm:**
    * `Node 1 (Classifier)`: Extracts emotion and forcefully translates phonetic Hindi tracking IDs (e.g., "ए डब्ल्यू बी वन टू थ्री") into standard alphanumeric AWBs (e.g., "AWB123").
    * `Node 2 (Database)`: Queries the local SQLite logistics database.
    * `Node 3 (Response)`: Sarvam-M drafts a 2-sentence empathetic Hinglish reply based on the DB result.
4. **Voice-Out:** Bulbul TTS converts the reply to audio bytes.
5. **Stream Back:** FastAPI returns the URL-encoded headers and audio stream to the frontend for auto-playback.

---

## 🚀 Live Deployment
* **Frontend:** [Link to your Streamlit Cloud app]
* **Backend:** Hosted on Render (Kept alive via UptimeRobot ping)

---

## 💻 Local Setup (Windows)

### 1. Get API Keys
Get your free API key from [dashboard.sarvam.ai](https://dashboard.sarvam.ai).
Create a `.env` file in the root directory:
```env
SARVAM_API_KEY=sk_your_actual_key_here


python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

uvicorn main:app --reload --port 8000

venv\Scripts\activate
streamlit run streamlit_app.py


🛠️ Build Hurdles Conquered
Dependency Clashes: Handled strict versioning conflicts between langchain-core and langgraph.

The Unicode Crash: Prevented fatal FastAPI 500 errors by URL-encoding raw Devanagari script in HTTP response headers.

TTS Payload Limits: Filtered out Sarvam-M's internal <think> reasoning tags via regex to prevent crashing the Bulbul TTS 500-character limit.

Phonetic Extraction: Engineered prompts to translate literal Hindi word-numbers into English alphanumeric database keys.