from fastapi import FastAPI
from pydantic import BaseModel
from ai import get_ai_reply
from datetime import datetime
from fastapi.responses import FileResponse

app = FastAPI()

# --------------------------------
# In-memory session storage
# --------------------------------
sessions = {}

# --------------------------------
# Context extraction helper
# --------------------------------
def extract_context(message: str, context: dict):
    msg = message.lower()

    # Room detection
    if "bedroom" in msg:
        context["room"] = "bedroom"
    elif "living room" in msg or "hall" in msg:
        context["room"] = "living room"
    elif "kitchen" in msg:
        context["room"] = "kitchen"

    # Budget detection
    if "lakh" in msg or "budget" in msg:
        context["budget"] = message

    # Style detection
    styles = ["modern", "minimal", "luxury", "traditional", "scandinavian"]
    for style in styles:
        if style in msg:
            context["style"] = style

    return context

# --------------------------------
# Request model
# --------------------------------
class ChatRequest(BaseModel):
    session_id: str
    message: str

# --------------------------------
# Routes
# --------------------------------
@app.get("/")
def read_root():
    return {"message": "Interior AI backend is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id
    user_message = request.message

    # Create new session if not exists
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "context": {},
            "last_active": None
        }

    session = sessions[session_id]

    # Store user message
    session["messages"].append({
        "role": "user",
        "content": user_message
    })

    # Extract and update context
    session["context"] = extract_context(user_message, session["context"])

    # Get AI reply with context
    ai_reply = get_ai_reply(user_message, session["context"])

    # Store AI reply
    session["messages"].append({
        "role": "assistant",
        "content": ai_reply
    })

    # Update last active time
    session["last_active"] = datetime.utcnow()

    return {
        "reply": ai_reply,
        "context": session["context"],
        "session_state": {
            "total_messages": len(session["messages"]),
            "last_active": session["last_active"]
        }
    }

# --------------------------------
# Admin APIs
# --------------------------------
@app.get("/admin/sessions")
def get_sessions():
    return {
        session_id: {
            "context": data["context"],
            "last_active": data["last_active"],
            "total_messages": len(data["messages"])
        }
        for session_id, data in sessions.items()
    }

@app.get("/admin/session/{session_id}")
def get_session_details(session_id: str):
    if session_id not in sessions:
        return {"error": "Session not found"}
    return sessions[session_id]

@app.get("/admin")
def admin_dashboard():
    return FileResponse("admin.html")

# --------------------------------
# Mock WhatsApp UI
# --------------------------------
@app.get("/chat-ui")
def chat_ui():
    return FileResponse("chat.html")
