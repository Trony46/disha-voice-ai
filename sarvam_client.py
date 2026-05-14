"""
sarvam_client.py
----------------
Thin wrappers around the three Sarvam AI APIs:
  1. Saaras  — Speech-to-Text (STT)
  2. Sarvam-M — LLM (chat completions, OpenAI-compatible)
  3. Bulbul v3 — Text-to-Speech (TTS)

Official docs: https://docs.sarvam.ai
"""

import os
import base64
import httpx
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
BASE_URL = "https://api.sarvam.ai"

# Shared auth header used by all three APIs
AUTH_HEADER = {"api-subscription-key": SARVAM_API_KEY}


# ---------------------------------------------------------------------------
# 1. STT — Saaras (Speech → Hinglish Text)
# ---------------------------------------------------------------------------

def transcribe_audio(audio_bytes: bytes, filename: str = "recording.wav") -> str:
    """
    Send raw audio bytes to the Saaras STT API.
    Returns the transcribed text (usually Hinglish or Hindi-leaning).

    Endpoint: POST /speech-to-text
    Docs: https://docs.sarvam.ai/api-reference-docs/speech-to-text
    """
    if not SARVAM_API_KEY:
        raise ValueError("SARVAM_API_KEY not set in .env file!")

    files = {
        "file": (filename, audio_bytes, "audio/wav"),
    }
    data = {
        "model": "saaras:v3",
        "language_code": "hi-IN",         #########
        "with_timestamps": "false",
    }

    with httpx.Client(timeout=60) as client:
        response = client.post(
            f"{BASE_URL}/speech-to-text",
            headers=AUTH_HEADER,
            files=files,
            data=data,
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"[STT Error] Status {response.status_code}: {response.text}"
        )

    result = response.json()
    transcript = result.get("transcript", "").strip()
    print(f"[STT] Transcribed: {transcript}")
    return transcript


# ---------------------------------------------------------------------------
# 2. LLM — Sarvam-M (Reasoning + Response Generation)
# ---------------------------------------------------------------------------

def call_sarvam_m(system_prompt: str, user_message: str, max_tokens: int = 400) -> str:
    if not SARVAM_API_KEY:
        raise ValueError("SARVAM_API_KEY not set in .env file!")

    headers = {**AUTH_HEADER, "Content-Type": "application/json"}
    payload = {
        "model": "sarvam-m",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    with httpx.Client(timeout=60) as client:
        response = client.post(
            f"{BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"[LLM Error] Status {response.status_code}: {response.text}"
        )

    reply = response.json()["choices"][0]["message"]["content"].strip()

    if "</think>" in reply:
        reply = reply.split("</think>")[-1].strip()

    print(f"[LLM] Reply: {reply}")
    return reply

# ---------------------------------------------------------------------------
# 3. TTS — Bulbul v3 (Hinglish Text → Audio Bytes)
# ---------------------------------------------------------------------------

def text_to_speech(text: str, speaker: str = "priya") -> bytes:
    if not SARVAM_API_KEY:
        raise ValueError("SARVAM_API_KEY not set in .env file!")

    headers = {**AUTH_HEADER, "Content-Type": "application/json"}
    payload = {
        "inputs": [text],
        "target_language_code": "hi-IN",
        "speaker": speaker,
        "model": "bulbul:v3",
        "enable_preprocessing": True,
        "speech_sample_rate": 22050,
    }

    with httpx.Client(timeout=60) as client:
        response = client.post(
            f"{BASE_URL}/text-to-speech",
            headers=headers,
            json=payload,
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"[TTS Error] Status {response.status_code}: {response.text}"
        )

    result = response.json()
    audio_b64 = result["audios"][0]
    audio_bytes = base64.b64decode(audio_b64)
    print(f"[TTS] Generated {len(audio_bytes)} bytes of audio.")
    return audio_bytes
