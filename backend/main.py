from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from ai import get_ai_reply
import os

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage
sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.get("/")
def root():
    return {"message": "Interior AI backend is running"}

# ✅ CHAT UI ROUTE (THIS FIXES 404)
@app.get("/chat-ui")
def chat_ui():
    file_path = os.path.join(os.path.dirname(__file__), "chat.html")
    return FileResponse(file_path)

@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id
    message = request.message

    if session_id not in sessions:
        sessions[session_id] = {
            "context": {},
            "messages": [],
            "last_active": None
        }

    session = sessions[session_id]
    reply = get_ai_reply(message, session["context"])

    session["messages"].append({"role": "user", "content": message})
    session["messages"].append({"role": "assistant", "content": reply})
    session["last_active"] = datetime.utcnow()

    return {
        "reply": reply,
        "context": session["context"],
        "session_state": {
            "total_messages": len(session["messages"]),
            "last_active": session["last_active"]
        }
    }
