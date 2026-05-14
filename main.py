import io
import urllib.parse
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from sarvam_client import transcribe_audio, text_to_speech
from agent import run_support_agent
from database import init_db

init_db()

app = FastAPI(
    title="Voice Support Bot",
    description="Hinglish voice support bot powered by Sarvam AI + LangGraph",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Voice Support Bot is running!"}

@app.post("/api/voice-support")
async def voice_support(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="No audio data received.")

    print(f"[API] Received audio: {len(audio_bytes)} bytes, filename: {audio.filename}")

    try:
        transcription = transcribe_audio(audio_bytes, filename=audio.filename or "recording.wav")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"STT failed: {str(e)}")

    if not transcription:
        raise HTTPException(status_code=422, detail="Could not transcribe audio — please speak clearly.")

    print(f"[API] Transcription: {transcription}")

    try:
        reply_text = run_support_agent(transcription)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Agent failed: {str(e)}")

    print(f"[API] Agent reply: {reply_text}")

    try:
        safe_reply_text = reply_text[:495]
        reply_audio = text_to_speech(safe_reply_text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TTS failed: {str(e)}")

    return StreamingResponse(
        io.BytesIO(reply_audio),
        media_type="audio/wav",
        headers={
            "X-Transcription": urllib.parse.quote(transcription[:200]),
            "X-Reply-Text": urllib.parse.quote(reply_text[:500]),
        },
    )

@app.get("/api/test-db")
def test_db():
    from database import get_shipment_status
    sample = get_shipment_status("AWB123")
    return {"test_awb": "AWB123", "result": sample}