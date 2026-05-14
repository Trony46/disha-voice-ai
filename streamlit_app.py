import io
import urllib.parse
import requests
import streamlit as st

FASTAPI_URL = "http://localhost:8000/api/voice-support"
PRODUCT_NAME = "Disha"
BUILDER_NAME = "Ashmit Shaw"
BUILDER_GITHUB = "https://github.com/Trony46"
BUILDER_LINKEDIN = "https://linkedin.com/in/ashmitshaw"

st.set_page_config(
    page_title="Disha — Hinglish Voice Support AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu          { visibility: hidden; }
.stDeployButton    { display: none !important; }
footer             { visibility: hidden; }
header             { visibility: hidden; }
.block-container   { padding-top: 2rem !important; padding-bottom: 3rem !important; }

:root {
    --bg:      #08080f;
    --surface: #111118;
    --card:    #16161f;
    --border:  #222230;
    --accent:  #f97316;
    --accent-hover: #ea580c;
    --accent2: #8b5cf6;
    --green:   #22c55e;
    --red:     #ef4444;
    --blue:    #3b82f6;
    --text:    #e2e8f0;
    --muted:   #64748b;
    --muted2:  #94a3b8;
}

.hero { text-align:center; padding:3.5rem 1rem 2.5rem; }
.hero-badge {
    display:inline-block;
    background:rgba(249,115,22,0.12);
    border:1px solid rgba(249,115,22,0.35);
    color:var(--accent);
    font-size:0.72rem; font-weight:600; letter-spacing:0.12em;
    text-transform:uppercase; padding:5px 14px; border-radius:100px; margin-bottom:1.4rem;
}
.hero-title {
    font-size:clamp(2.6rem,5vw,4rem); font-weight:700; color:#ffffff;
    line-height:1.1; margin:0 0 0.8rem; letter-spacing:-0.02em;
}
.hero-title span { color:var(--accent); }
.hero-sub-main {
    font-size:1.2rem; color:#e2e8f0; max-width:650px;
    margin:0 auto 0.5rem; line-height:1.5; font-weight:500;
}
.hero-sub {
    font-size:1rem; color:var(--muted2); max-width:600px;
    margin:0 auto 2rem; line-height:1.65; font-weight:400;
}

.cta-btn {
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff !important;
    font-size: 1.05rem;
    font-weight: 600;
    padding: 14px 32px;
    border-radius: 8px;
    text-decoration: none;
    margin-top: 1.5rem;
    transition: all 0.2s ease;
    border: 1px solid #ea580c;
}
.cta-btn:hover {
    background-color: var(--accent-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.pill-row { display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:0.5rem; }
.pill {
    background:var(--card); border:1px solid var(--border);
    color:var(--muted2); font-size:0.75rem; font-weight:500;
    padding:5px 13px; border-radius:100px;
}
.pill b { color:var(--text); }

.section-label {
    font-size:0.7rem; font-weight:700; letter-spacing:0.14em;
    text-transform:uppercase; color:var(--muted); margin-bottom:0.8rem;
}
.section-title { font-size:1.5rem; font-weight:700; color:var(--text); margin-bottom:0.4rem; }
.section-desc  { font-size:0.9rem; color:var(--muted2); line-height:1.6; margin-bottom:1.6rem; }

.flow-wrap {
    display:flex; align-items:flex-start; gap:0;
    overflow-x:auto; padding-bottom:0.5rem;
}
.flow-step {
    background:var(--card); border:1px solid var(--border);
    border-radius:12px; padding:18px 20px; min-width:160px; flex:1;
}
.flow-num { font-size:0.65rem; font-weight:700; letter-spacing:0.1em; color:var(--accent); margin-bottom:8px; text-transform:uppercase; }
.flow-icon { font-size:1.4rem; margin-bottom:6px; }
.flow-name { font-size:0.85rem; font-weight:600; color:var(--text); margin-bottom:4px; }
.flow-detail { font-size:0.75rem; color:var(--muted2); line-height:1.5; }
.flow-arrow { color:var(--border); font-size:1.2rem; padding:0 6px; align-self:center; flex-shrink:0; }

.demo-tip {
    background:rgba(249,115,22,0.08); border:1px solid rgba(249,115,22,0.2);
    border-radius:10px; padding:12px 16px; font-size:0.82rem;
    color:var(--muted2); margin-bottom:1.4rem; line-height:1.6;
}
.demo-tip b { color:var(--accent); }

.result-card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:12px; padding:1.2rem 1.4rem; margin-top:1rem;
}
.result-label { font-size:0.65rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--muted); margin-bottom:0.5rem; }
.transcript-text { font-size:0.95rem; color:#93c5fd; font-style:italic; line-height:1.55; }
.reply-text { font-size:0.95rem; color:var(--text); line-height:1.65; }
.status-pill { display:inline-block; font-size:0.7rem; font-weight:600; padding:3px 10px; border-radius:100px; margin-bottom:8px; }
.status-ok  { background:rgba(34,197,94,0.15);  color:var(--green); }
.status-err { background:rgba(239,68,68,0.15);   color:var(--red);   }

.awb-table { width:100%; border-collapse:collapse; font-size:0.82rem; }
.awb-table thead tr { border-bottom:1px solid var(--border); }
.awb-table th { text-align:left; color:var(--muted); font-weight:600; font-size:0.7rem; letter-spacing:0.08em; text-transform:uppercase; padding:8px 12px; }
.awb-table td { padding:9px 12px; color:var(--muted2); border-bottom:1px solid rgba(34,40,55,0.6); vertical-align:top; }
.awb-table td:first-child { font-family:'Courier New',monospace; font-weight:600; color:var(--accent); }
.badge { display:inline-block; font-size:0.68rem; font-weight:600; padding:2px 8px; border-radius:4px; }
.badge-delay   { background:rgba(239,68,68,0.15);   color:#fca5a5; }
.badge-transit { background:rgba(59,130,246,0.15);  color:#93c5fd; }
.badge-ofd     { background:rgba(249,115,22,0.15);  color:#fdba74; }
.badge-customs { background:rgba(139,92,246,0.15);  color:#c4b5fd; }
.badge-done    { background:rgba(34,197,94,0.15);   color:#86efac; }
.badge-lost    { background:rgba(239,68,68,0.2);    color:#f87171; }

.hurdle-card {
    background:var(--card); border:1px solid var(--border);
    border-left:3px solid var(--accent2); border-radius:10px;
    padding:16px 18px; margin-bottom:12px;
}
.hurdle-prob  { font-size:0.75rem; font-weight:600; color:#f87171; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:5px; }
.hurdle-title { font-size:0.92rem; font-weight:600; color:var(--text); margin-bottom:6px; }
.hurdle-body  { font-size:0.82rem; color:var(--muted2); line-height:1.6; margin-bottom:8px; }
.hurdle-fix   { font-size:0.78rem; color:#86efac; background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.15); border-radius:6px; padding:8px 12px; line-height:1.55; }
.hurdle-fix b { color:#4ade80; }

.thin-divider { border:none; border-top:1px solid var(--border); margin:2.5rem 0; }

.footer { text-align:center; padding:2rem 0 1rem; }
.footer-name { font-size:0.82rem; color:var(--muted); margin-bottom:6px; }
.footer-name a { color:var(--accent); text-decoration:none; }
.footer-links { font-size:0.75rem; color:var(--muted); }
.footer-links a { color:var(--muted2); text-decoration:none; margin:0 8px; }
.powered-row { display:flex; gap:10px; justify-content:center; margin-top:14px; flex-wrap:wrap; }
.powered-pill { background:var(--card); border:1px solid var(--border); border-radius:100px; padding:5px 14px; font-size:0.72rem; color:var(--muted2); }
.powered-pill b { color:var(--text); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-badge">🇮🇳 Built for Bharat &nbsp;·&nbsp; Voice-First &nbsp;·&nbsp; Autonomous Swarm</div>
  <h1 class="hero-title"><span>Disha</span> — The Hinglish Support AI</h1>
  <p class="hero-sub-main">
    Western AIs don't understand our desi slang, and local uncles hate typing on apps. 
  </p>
  <p class="hero-sub">
    Disha is an autonomous multi-agent swarm that listens to raw, angry Hinglish voice notes, understands the intent, securely queries your logistics database, and replies in a calming Indian voice. <b>Zero typing required.</b>
  </p>
  <div class="pill-row">
    <span class="pill">🎙️ <b>Saaras v3</b> STT</span>
    <span class="pill">🧠 <b>Sarvam-M</b> LLM</span>
    <span class="pill">🔊 <b>Bulbul v3</b> TTS</span>
    <span class="pill">🔗 <b>LangGraph</b> Multi-Agent</span>
    <span class="pill">⚡ <b>FastAPI</b> Backend</span>
  </div>
  <a href="#live-demo" target="_self" class="cta-btn">Jump to Live Demo 🎙️</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Architecture</p>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">How it works</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-desc">Five stages, three Sarvam APIs, one LangGraph swarm — from raw audio to a calm Indian voice reply in under 15 seconds.</p>', unsafe_allow_html=True)

st.markdown("""
<div class="flow-wrap">
  <div class="flow-step">
    <div class="flow-num">Step 01</div>
    <div class="flow-icon">🎙️</div>
    <div class="flow-name">Record</div>
    <div class="flow-detail">Streamlit captures mic audio as <code>.wav</code> and POSTs it to FastAPI <code>/api/voice-support</code></div>
  </div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">
    <div class="flow-num">Step 02</div>
    <div class="flow-icon">📝</div>
    <div class="flow-name">Saaras STT</div>
    <div class="flow-detail">Sarvam <b>Saaras v3</b> transcribes audio into Hinglish — handles angry accents and phonetic AWB spellings</div>
  </div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">
    <div class="flow-num">Step 03</div>
    <div class="flow-icon">🧠</div>
    <div class="flow-name">LangGraph Swarm</div>
    <div class="flow-detail"><b>Node 1</b> classifies emotion + extracts AWB → <b>Node 2</b> queries SQLite → <b>Node 3</b> crafts empathy reply</div>
  </div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">
    <div class="flow-num">Step 04</div>
    <div class="flow-icon">🔊</div>
    <div class="flow-name">Bulbul TTS</div>
    <div class="flow-detail">Sarvam <b>Bulbul v3</b> converts the Hinglish reply into a natural Indian voice WAV</div>
  </div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">
    <div class="flow-num">Step 05</div>
    <div class="flow-icon">📤</div>
    <div class="flow-name">Stream Back</div>
    <div class="flow-detail">FastAPI streams WAV bytes back; Streamlit auto-plays the reply audio in your browser</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

st.markdown('<div id="live-demo"></div>', unsafe_allow_html=True)

left, right = st.columns([1.1, 1], gap="large")

with left:
    st.markdown('<p class="section-label">Live Demo</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Try it now</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="demo-tip">
      <b>How to use:</b><br>
      1. Click the microphone below 🎙️<br>
      2. Speak your complaint in Hinglish — mention an AWB number<br>
      3. Stop recording — Disha will think and reply in ~10–15 sec<br><br>
      <b>Example phrases to try:</b><br>
      <i>"Bhai AWB123 kahan hai, ek hafte se nahi aaya!"</i><br>
      <i>"Mera AWB001 abhi tak deliver nahi hua, kya ho raha hai?!"</i><br>
      <i>"AWB999 lost ho gaya kya, koi batata nahi!"</i>
    </div>
    """, unsafe_allow_html=True)

    backend_url = st.text_input(
        "Backend URL",
        value=FASTAPI_URL,
        help="Change this if FastAPI is running on a different port.",
    )
    audio_input = st.audio_input(
        label="🎙️  Click to record — speak your complaint in Hinglish",
        key="audio_recorder",
    )

with right:
    st.markdown('<p class="section-label">Response</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Disha replies</h2>', unsafe_allow_html=True)

    response_placeholder = st.empty()

    if audio_input is None:
        response_placeholder.markdown("""
        <div style="
            background:#111118; border:1px dashed #222230; border-radius:14px;
            padding:3rem 2rem; text-align:center; color:#334155; font-size:0.9rem;
        ">
            🎙️<br><br>
            Record something on the left<br>to see Disha's reply here
        </div>
        """, unsafe_allow_html=True)

if audio_input is not None:
    with right:
        with st.spinner("Disha is thinking..."):
            try:
                audio_bytes  = audio_input.read()
                files        = {"audio": ("recording.wav", audio_bytes, "audio/wav")}
                api_response = requests.post(backend_url, files=files, timeout=90)

                if api_response.status_code == 200:
                    transcription = urllib.parse.unquote(api_response.headers.get("X-Transcription", ""))
                    reply_text    = urllib.parse.unquote(api_response.headers.get("X-Reply-Text", ""))

                    response_placeholder.empty()

                    if transcription:
                        st.markdown(
                            '<div class="result-card">'
                            '<div class="result-label">📝 What we heard</div>'
                            f'<p class="transcript-text">"{transcription}"</p>'
                            '</div>',
                            unsafe_allow_html=True,
                        )
                    if reply_text:
                        st.markdown(
                            '<div class="result-card" style="border-left:3px solid #f97316;">'
                            '<div class="result-label">🤖 Disha says</div>'
                            f'<p class="reply-text">{reply_text}</p>'
                            '</div>',
                            unsafe_allow_html=True,
                        )

                    st.markdown("**🔊 Audio reply:**")
                    st.audio(io.BytesIO(api_response.content), format="audio/wav", autoplay=True)
                    st.markdown('<span class="status-pill status-ok">✓ Response complete</span>', unsafe_allow_html=True)

                elif api_response.status_code == 422:
                    st.warning("⚠️ Audio unclear — please speak louder and try again.")
                else:
                    detail = api_response.json().get("detail", api_response.text)
                    st.error(f"Server error {api_response.status_code}: {detail}")

            except requests.exceptions.ConnectionError:
                st.markdown(
                    '<div class="result-card">'
                    '<span class="status-pill status-err">✗ Connection failed</span><br><br>'
                    '<span style="font-size:0.85rem;color:#94a3b8;">'
                    'FastAPI backend is not running.<br><br>Start it with:<br>'
                    '<code style="color:#fdba74;">uvicorn main:app --reload --port 8000</code>'
                    '</span></div>',
                    unsafe_allow_html=True,
                )
            except requests.exceptions.Timeout:
                st.error("Request timed out — Sarvam API is slow. Try again.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Documentation</p>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">System reference</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-desc">Everything you need to test, understand, and extend Disha.</p>', unsafe_allow_html=True)

doc_tab1, doc_tab2, doc_tab3 = st.tabs(["📦  Mock Shipment Data", "🏗️  Backend Architecture", "🔧  Project Hurdles"])

with doc_tab1:
    st.markdown("""
    <p style="font-size:0.85rem;color:#64748b;margin-bottom:1.2rem;">
      Disha runs on a local SQLite database (<code>logistics.db</code>) seeded with these mock shipments.
      Mention any AWB number in your voice complaint to trigger a DB lookup and get real details back.
    </p>
    <table class="awb-table">
      <thead><tr>
        <th>AWB Number</th><th>Customer</th><th>Status</th>
        <th>Location</th><th>ETA</th><th>Reason</th>
      </tr></thead>
      <tbody>
        <tr><td>AWB001</td><td>Ramesh Sharma</td><td><span class="badge badge-delay">Delayed</span></td><td>Delhi Hub</td><td>2 days</td><td>Heavy rain causing road blockage in Delhi NCR</td></tr>
        <tr><td>AWB002</td><td>Priya Verma</td><td><span class="badge badge-transit">In Transit</span></td><td>Lucknow Facility</td><td>Tomorrow 6 PM</td><td>On time, shipment moving normally</td></tr>
        <tr><td>AWB003</td><td>Suresh Gupta</td><td><span class="badge badge-ofd">Out for Delivery</span></td><td>Your City</td><td>Today by 9 PM</td><td>Package is with the delivery agent</td></tr>
        <tr><td>AWB004</td><td>Anita Patel</td><td><span class="badge badge-customs">Stuck at Customs</span></td><td>Mumbai Airport</td><td>3–5 days</td><td>Documentation verification in progress</td></tr>
        <tr><td>AWB005</td><td>Vijay Kumar</td><td><span class="badge badge-done">Delivered</span></td><td>Delivered</td><td>—</td><td>Package delivered successfully on Monday</td></tr>
        <tr><td>AWB123</td><td>Angry Uncle Ji</td><td><span class="badge badge-delay">Delayed</span></td><td>Ghaziabad Depot</td><td>3 days</td><td>Vehicle breakdown near NH-9; rerouting in progress</td></tr>
        <tr><td>AWB999</td><td>Test User</td><td><span class="badge badge-lost">Lost</span></td><td>Unknown</td><td>Unknown</td><td>We are investigating the shipment location</td></tr>
      </tbody>
    </table>
    <br>
    <p style="font-size:0.78rem;color:#475569;">
      💡 <b>No AWB in your speech?</b> The LangGraph router skips the DB node entirely — Disha will politely ask you for your tracking number.
    </p>
    """, unsafe_allow_html=True)

with doc_tab2:
    st.markdown('<p style="font-size:0.85rem;color:#64748b;margin-bottom:1.4rem;">A quick walkthrough of each backend file and what it does.</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        st.markdown("""
**`main.py` — FastAPI Orchestrator**

Single endpoint: `POST /api/voice-support`
1. Receives `.wav` from Streamlit
2. Calls Saaras STT → transcript
3. Runs `agent.run_support_agent(transcript)`
4. Calls Bulbul TTS → WAV bytes
5. Streams WAV back with URL-encoded Hindi headers

Also exposes `/api/test-db` and `/docs` (auto Swagger UI).

---

**`sarvam_client.py` — API Wrappers**

Three clean functions:
- `transcribe_audio(bytes)` → Saaras v3
- `call_sarvam_m(system, user)` → Sarvam-M
- `text_to_speech(text)` → Bulbul v3

All auth via `api-subscription-key` header. 60s timeout.
        """)

    with col_b:
        st.markdown("""
**`agent.py` — LangGraph Swarm**

SupportState (TypedDict)
├─ user_audio_text
├─ detected_emotion
├─ extracted_awb
├─ logistics_status
└─ agent_reply_text

Graph:
START → classify_intent
├─ (AWB found) → lookup_logistics → generate_response
└─ (no AWB)   → generate_response → END

---
**`database.py` — Mock SQLite**
Auto-creates `logistics.db` on first import. 
`get_shipment_status(awb)` does a case-insensitive lookup and returns a dict or `None`.
        """)

with doc_tab3:
    st.markdown('<p style="font-size:0.85rem;color:#64748b;margin-bottom:1.4rem;">Real bugs hit during the build sprint — and exactly how they were fixed.</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="hurdle-card">
  <div class="hurdle-prob">Hurdle 01 · Dependency Clash</div>
  <div class="hurdle-title">LangGraph rejecting LangChain-core at startup</div>
  <div class="hurdle-body">The pinned <code>langchain-core</code> version was incompatible with the newer <code>langgraph</code> — the server refused to start before any code ran.</div>
  <div class="hurdle-fix"><b>Fix:</b> Wiped the venv, manually bumped <code>langchain-core</code> to the compatible range, fresh <code>pip install -r requirements.txt</code>. Aligned on the second attempt.</div>
</div>
<div class="hurdle-card">
  <div class="hurdle-prob">Hurdle 02 · Sarvam Silent Breaking Changes</div>
  <div class="hurdle-title">saaras:v2 and TTS voice "meera" removed without notice</div>
  <div class="hurdle-body">API calls immediately returned 422/404. Sarvam deprecated <code>saaras:v2</code> and several TTS speakers without a migration notice.</div>
  <div class="hurdle-fix"><b>Fix:</b> Checked live Sarvam docs, updated STT to <code>saaras:v3</code> and swapped TTS speaker to an active voice. Both resumed immediately.</div>
</div>
<div class="hurdle-card">
  <div class="hurdle-prob">Hurdle 03 · Double Backend Crash</div>
  <div class="hurdle-title">&lt;think&gt; tags broke TTS; Hindi headers crashed FastAPI</div>
  <div class="hurdle-body">Sarvam-M prefixes replies with long <code>&lt;think&gt;...&lt;/think&gt;</code> reasoning blocks — sending those raw to Bulbul exceeded the 500-char TTS limit. Simultaneously, FastAPI threw <code>UnicodeEncodeError</code> on raw Hindi in HTTP headers.</div>
  <div class="hurdle-fix"><b>Fix:</b> Regex filter strips <code>&lt;think&gt;</code> blocks before TTS, string capped at safe length. Headers wrapped with <code>urllib.parse.quote()</code> server-side, <code>unquote()</code> client-side.</div>
</div>
<div class="hurdle-card">
  <div class="hurdle-prob">Hurdle 04 · Phonetic Hindi AWB Gap</div>
  <div class="hurdle-title">STT returned "ए डब्ल्यू बी वन टू थ्री" — regex missed it completely</div>
  <div class="hurdle-body">When AWB numbers were spoken aloud, Saaras transcribed them phonetically in Hindi script. The <code>AWB\d+</code> regex matched nothing — router skipped DB lookup and Disha looped asking for the number.</div>
  <div class="hurdle-fix"><b>Fix:</b> Increased classifier token budget and added a strict prompt forcing Sarvam-M to transliterate phonetic Hindi spellings into standard alphanumeric format (AWB123) before returning structured output.</div>
</div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
st.markdown(f"""
<div class="footer">
  <p class="footer-name">
    Built by &nbsp;<a href="{BUILDER_LINKEDIN}" target="_blank"><b>{BUILDER_NAME}</b></a>
  </p>
  <div class="footer-links">
    <a href="{BUILDER_GITHUB}" target="_blank">GitHub</a>
    <a href="{BUILDER_LINKEDIN}" target="_blank">LinkedIn</a>
    <a href="https://docs.sarvam.ai" target="_blank">Sarvam Docs</a>
    <a href="http://localhost:8000/docs" target="_blank">API Docs ↗</a>
  </div>
  <div class="powered-row">
    <span class="powered-pill">🎙️ <b>Saaras v3</b> — STT</span>
    <span class="powered-pill">🧠 <b>Sarvam-M</b> — LLM (free)</span>
    <span class="powered-pill">🔊 <b>Bulbul v3</b> — TTS</span>
    <span class="powered-pill">🔗 <b>LangGraph</b> — Swarm</span>
    <span class="powered-pill">⚡ <b>FastAPI</b> — Backend</span>
  </div>
</div>
""", unsafe_allow_html=True)