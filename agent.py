"""
agent.py
--------
LangGraph-powered multi-agent support brain.

Graph flow:
  START
    └─► [Node 1] classify_intent
          ├─► (AWB found)  ──► [Node 2] lookup_logistics ──► [Node 3] generate_response
          └─► (no AWB)     ──────────────────────────────► [Node 3] generate_response
                                                                  └─► END
"""

import re
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from sarvam_client import call_sarvam_m
from database import get_shipment_status


# ---------------------------------------------------------------------------
# State schema — passed between every node in the graph
# ---------------------------------------------------------------------------

class SupportState(TypedDict):
    user_audio_text: str               # Raw transcription from Saaras STT
    detected_emotion: str              # "angry" | "frustrated" | "calm" | "neutral"
    extracted_awb: Optional[str]       # e.g. "AWB123" or None
    logistics_status: Optional[str]    # Human-readable status from DB
    agent_reply_text: str              # Final Hinglish text reply
    reply_audio_bytes: Optional[bytes] # TTS bytes (filled in by FastAPI, not here)


# ---------------------------------------------------------------------------
# Node 1: Intent Classifier
# Detects emotion AND extracts AWB number from the transcription
# ---------------------------------------------------------------------------

CLASSIFIER_SYSTEM_PROMPT = """
You are an intent analysis assistant for an Indian logistics company.
You will receive a customer message (usually in Hinglish or Hindi script).

Your job is to extract two things:
1. The customer's EMOTION: one of [angry, frustrated, calm, neutral]
2. Any AWB/tracking number mentioned. CRITICAL: If the user speaks the tracking number in Hindi words (e.g., "ए डब्ल्यू बी वन टू थ्री" or "A W B one two three"), you MUST convert it to standard English alphanumeric format (e.g., "AWB123"). Return "NONE" if not found.

Respond ONLY in this exact format at the very end of your response:
EMOTION: <emotion>
AWB: <awb_number_or_NONE>
"""

def classify_intent(state: SupportState) -> SupportState:
    """
    Node 1: Analyze the transcription for emotion and tracking number.
    Updates: detected_emotion, extracted_awb
    """
    print("[Agent] Node 1: classify_intent running...")

    text = state["user_audio_text"]

    # --- Try regex extraction first (fast, no API cost) ---
    awb_pattern = re.compile(r'\b(AWB\d{3,}|TRK\d{3,}|[A-Z]{2,4}\d{4,})\b', re.IGNORECASE)
    regex_match = awb_pattern.search(text)

    # --- Call LLM for emotion + confirmatory AWB extraction ---
    llm_response = call_sarvam_m(
        system_prompt=CLASSIFIER_SYSTEM_PROMPT,
        user_message=text,
        max_tokens=400,
    )

    # Parse LLM response
    emotion = "neutral"
    llm_awb = None

    for line in llm_response.strip().splitlines():
        line = line.strip()
        if line.upper().startswith("EMOTION:"):
            emotion = line.split(":", 1)[1].strip().lower()
        elif line.upper().startswith("AWB:"):
            val = line.split(":", 1)[1].strip().upper()
            if val != "NONE" and val:
                llm_awb = val

    # Regex result wins if LLM missed it
    final_awb = llm_awb or (regex_match.group(0).upper() if regex_match else None)

    print(f"[Agent] Emotion: {emotion} | AWB: {final_awb}")

    return {
        **state,
        "detected_emotion": emotion,
        "extracted_awb": final_awb,
    }


# ---------------------------------------------------------------------------
# Node 2: Logistics Tool
# Queries the mock SQLite DB using the extracted AWB number
# ---------------------------------------------------------------------------

def lookup_logistics(state: SupportState) -> SupportState:
    """
    Node 2: Fetch shipment status from the mock DB.
    Updates: logistics_status
    """
    print("[Agent] Node 2: lookup_logistics running...")

    awb = state.get("extracted_awb")

    if not awb:
        return {**state, "logistics_status": None}

    shipment = get_shipment_status(awb)

    if shipment:
        status_text = (
            f"AWB Number: {shipment['awb_number']}\n"
            f"Customer: {shipment['customer_name']}\n"
            f"Status: {shipment['status']}\n"
            f"Current Location: {shipment['location']}\n"
            f"Expected Delivery: {shipment['expected_delivery']}\n"
            f"Reason: {shipment['reason']}"
        )
        print(f"[Agent] Found shipment:\n{status_text}")
    else:
        status_text = f"No shipment found for AWB number: {awb}"
        print(f"[Agent] {status_text}")

    return {**state, "logistics_status": status_text}


# ---------------------------------------------------------------------------
# Node 3: Empathy & Response Agent
# Generates a calm, helpful Hinglish response using Sarvam-M
# ---------------------------------------------------------------------------

RESPONSE_SYSTEM_PROMPT = """
You are "Disha", a warm and empathetic customer support agent for FastShip Logistics India.
The customer is speaking in Hinglish.

Rules you MUST follow:
1. ALWAYS reply in short, conversational Hinglish (mix Hindi + English naturally).
2. STRICT RULE: Keep the entire reply UNDER 2 short sentences. NEVER exceed 350 characters.
3. If the customer is angry, acknowledge it quickly: "Haan bhai, delay samajh sakti hoon."
4. Give the tracking update quickly and warmly.
5. NEVER reply in pure Hindi or pure English.
"""

def generate_response(state: SupportState) -> SupportState:
    print("[Agent] Node 3: generate_response running...")

    emotion = state.get("detected_emotion", "neutral")
    logistics_info = state.get("logistics_status", None)
    user_text = state["user_audio_text"]

    context_parts = [f"Customer message: {user_text}"]
    context_parts.append(f"Customer emotion: {emotion}")

    if logistics_info:
        context_parts.append(f"\nShipment details from our system:\n{logistics_info}")
    else:
        context_parts.append(
            "\nNo tracking number was provided or found in the system. "
            "Ask the customer politely for their AWB/tracking number."
        )

    full_context = "\n".join(context_parts)

    reply = call_sarvam_m(
        system_prompt=RESPONSE_SYSTEM_PROMPT,
        user_message=full_context,
        max_tokens=400,
    )

    return {**state, "agent_reply_text": reply}

# ---------------------------------------------------------------------------
# Routing function — decides whether to skip logistics lookup
# ---------------------------------------------------------------------------

def route_after_classifier(state: SupportState) -> str:
    """Route to logistics lookup if AWB found, else go straight to response."""
    if state.get("extracted_awb"):
        return "lookup_logistics"
    return "generate_response"


# ---------------------------------------------------------------------------
# Build the LangGraph
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    graph = StateGraph(SupportState)

    # Add nodes
    graph.add_node("classify_intent",   classify_intent)
    graph.add_node("lookup_logistics",  lookup_logistics)
    graph.add_node("generate_response", generate_response)

    # Set entry point
    graph.set_entry_point("classify_intent")

    # Conditional routing after classification
    graph.add_conditional_edges(
        "classify_intent",
        route_after_classifier,
        {
            "lookup_logistics":  "lookup_logistics",
            "generate_response": "generate_response",
        },
    )

    # After DB lookup, always go to response
    graph.add_edge("lookup_logistics", "generate_response")

    # Response is the final node
    graph.add_edge("generate_response", END)

    return graph.compile()


# Compile once at import time — reused for every request
support_graph = build_graph()
print("[Agent] LangGraph compiled successfully.")


# ---------------------------------------------------------------------------
# Public function — called by FastAPI
# ---------------------------------------------------------------------------

def run_support_agent(transcribed_text: str) -> str:
    """
    Entry point: takes the STT transcription, runs it through the graph,
    and returns the final Hinglish reply text.
    """
    initial_state: SupportState = {
        "user_audio_text":   transcribed_text,
        "detected_emotion":  "neutral",
        "extracted_awb":     None,
        "logistics_status":  None,
        "agent_reply_text":  "",
        "reply_audio_bytes": None,
    }

    final_state = support_graph.invoke(initial_state)
    return final_state["agent_reply_text"]
