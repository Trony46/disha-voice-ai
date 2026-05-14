<div align="center">

# Disha — Hinglish Voice Support AI

*Speak angry Hinglish. Get a calm reply. Zero typing.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-FF6B35?style=flat)](https://langchain-ai.github.io/langgraph/)
[![Sarvam AI](https://img.shields.io/badge/Sarvam%20AI-Powered-6C3EE8?style=flat)](https://sarvam.ai)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)

**[🌐 Live App](https://disha-voice-ai.streamlit.app)**
</div>

---

Disha is a voice-native support agent that understands how Indians actually talk. You speak your complaint in Hinglish — she transcribes it, figures out your emotion, pulls your shipment status from a database, and replies back in a calm Indian voice. Under 15 seconds, start to finish.

---

## Stack

| | |
|---|---|
| **STT** | Sarvam Saaras v3 |
| **LLM** | Sarvam-M |
| **TTS** | Sarvam Bulbul v3 |
| **Agents** | LangGraph |
| **Backend** | FastAPI |
| **Frontend** | Streamlit |
| **DB** | SQLite |

---

## How it works

```
mic input (.wav)
      │
      ▼
Saaras v3 STT  ──►  Hinglish transcript
      │
      ▼
LangGraph Swarm
  ├── Node 1: classify_intent
  │     detects emotion + extracts AWB number
  │     (translates phonetic Hindi "ए डब्ल्यू बी" → "AWB123")
  │
  ├── Node 2: lookup_logistics        (skipped if no AWB found)
  │     queries SQLite for shipment status
  │
  └── Node 3: generate_response
        Sarvam-M writes empathetic Hinglish reply
      │
      ▼
Bulbul v3 TTS  ──►  WAV audio bytes
      │
      ▼
streamed back to browser → auto-plays
```

### Agent State

```python
class SupportState(TypedDict):
    user_audio_text:   str
    detected_emotion:  str            # angry | frustrated | calm | neutral
    extracted_awb:     Optional[str]  # AWB123 or None
    logistics_status:  Optional[str]  # result from DB
    agent_reply_text:  str
```

---

## Mock Data

Pre-seeded SQLite DB with these shipments — use any AWB number in your complaint:

| AWB | Status | Location | Note |
|---|---|---|---|
| `AWB001` | 🔴 Delayed | Delhi Hub | Rain, road blockage |
| `AWB002` | 🔵 In Transit | Lucknow | On time |
| `AWB003` | 🟠 Out for Delivery | Your City | With agent |
| `AWB004` | 🟣 Customs Hold | Mumbai Airport | Docs pending |
| `AWB005` | 🟢 Delivered | — | Done |
| `AWB123` | 🔴 Delayed | Ghaziabad Depot | NH-9 breakdown |
| `AWB999` | 🔴 Lost | Unknown | Under investigation |

**Try saying:**
```
"Bhai AWB123 kahan hai, ek hafte se nahi aaya!"
"Mera AWB999 lost ho gaya kya?!"
```

> No AWB in your speech? The router skips the DB node and Disha asks you for it politely.

---

## Local Setup

```bash
git clone https://github.com/Trony46/disha-voice-support
cd disha-voice-support

python -m venv venv && venv\Scripts\activate   # Windows
pip install -r requirements.txt

cp .env.example .env   # add your SARVAM_API_KEY
```

Get a free key at [dashboard.sarvam.ai](https://dashboard.sarvam.ai).

```bash
# Terminal 1 — backend
uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
streamlit run streamlit_app.py
```

---

## API

### `POST /api/voice-support`

Runs the full pipeline. Accepts `.wav`, returns `audio/wav` stream.

| Header (response) | Description |
|---|---|
| `X-Transcription` | URL-encoded transcript of user speech |
| `X-Reply-Text` | URL-encoded Hinglish reply text |

Other endpoints: `GET /` health check · `GET /api/test-db` · `GET /docs` Swagger UI

---

## Bugs I Hit

**1. Dependency clash** — newer `langgraph` rejected the pinned `langchain-core`. Fixed by bumping to the compatible version range and doing a clean reinstall.

**2. Sarvam silent deprecations** — `saaras:v2` and the `meera` TTS voice were removed without notice. Updated to `saaras:v3` and a working speaker.

**3. `<think>` tags broke TTS** — Sarvam-M outputs reasoning inside `<think>` blocks which blew past Bulbul's 500-char limit. Stripped with regex before hitting TTS. Also hit `UnicodeEncodeError` sending raw Hindi in HTTP headers — fixed with `urllib.parse.quote/unquote` on both ends.

**4. Phonetic Hindi AWB gap** — Saaras transcribed "AWB123" as `ए डब्ल्यू बी वन टू थ्री`. Regex missed it entirely. Fixed by prompting Sarvam-M to transliterate phonetic Hindi into alphanumeric before the regex runs.

---

## Project Structure

```
├── main.py            # FastAPI — pipeline orchestration
├── agent.py           # LangGraph — 3-node swarm
├── sarvam_client.py   # Saaras / Sarvam-M / Bulbul wrappers
├── database.py        # SQLite mock DB
├── streamlit_app.py   # Frontend
├── requirements.txt
└── .env.example
```

---
