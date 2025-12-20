from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from ai import get_ai_reply

app = FastAPI()

# -----------------------------
# Base directory (IMPORTANT)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

# -----------------------------
# In-memory session storage
# -----------------------------
sessions = {}

# -----------------------------
# Context extraction helper
# -----------------------------
def extract_context(message: str, context: dict):
    msg = message.lower()

    if "bedroom" in msg:
        context["room"] = "bedroom"
    elif "living room" in msg or "hall" in msg:
        context["room"] = "living room"
    elif "kitchen" in msg:
        context["room"] = "kitchen"

    styles = ["modern", "minimal", "luxury", "traditional", "scandinavian"]
    for style in styles:
        if style in msg:
            context["style"] = style

    return context

# -----------------------------
# Request model
# -----------------------------
class ChatRequest(BaseModel):
    session_id: str
    message: str

# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "Interior AI backend is running"}

# -----------------------------
# Chat API
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id
    user_message = request.message

    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "context": {},
            "last_active": None
        }

    session = sessions[session_id]

    session["messages"].append({
        "role": "user",
        "content": user_message
    })

    session["context"] = extract_context(user_message, session["context"])

    ai_reply = get_ai_reply(user_message, session["context"])

    session["messages"].append({
        "role": "assistant",
        "content": ai_reply
    })

    session["last_active"]_]()
