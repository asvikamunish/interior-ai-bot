from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime

from ai import get_ai_reply

app = FastAPI()

# -----------------------------
# Templates (IMPORTANT)
# -----------------------------
templates = Jinja2Templates(directory="templates")

# -----------------------------
# In-memory session storage
# -----------------------------
sessions = {}

# -----------------------------
# Request model
# -----------------------------
class ChatRequest(BaseModel):
    session_id: str
    message: str

# -----------------------------
# Helper: context extraction
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
# Routes
# -----------------------------
@app.get("/")
def root():
    return {"message": "Interior AI backend is running"}

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

    reply = get_ai_reply(user_message, session["context"])

    session["messages"].append({
        "role": "assistant",
        "content": reply
    })

    session["last_active"] = datetime.utcnow()

    return {
        "reply": reply,
        "context": session["context"],
        "session_state": {
            "total_messages": len(session["messages"]),
            "last_active": session["last_active"]
        }
    }

# -----------------------------
# UI Routes (THIS FIXES CHAT UI)
# -----------------------------
@app.get("/chat-ui")
def chat_ui(request: Request):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request}
    )

@app.get("/admin")
def admin_ui(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {"request": request}
    )

# -----------------------------
# Admin APIs
# -----------------------------
@app.get("/admin/sessions")
def get_sessions():
    return {
        sid: {
            "context": data["context"],
            "last_active": data["last_active"],
            "total_messages": len(data["messages"])
        }
        for sid, data in sessions.items()
    }
