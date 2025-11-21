from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

# ---------------------------------------
# FastAPI App
# ---------------------------------------
app = FastAPI(title="Cyber Security Chatbot API")

# ---------------------------------------
# Load JSON file (READ ONLY)
# ---------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE = os.path.join(BASE_DIR, "cyber_data.json")

# Load data safely
try:
    with open(JSON_FILE, "r") as f:
        CYBER_DATA = json.load(f)
except Exception:
    CYBER_DATA = {"responses": {}}

RESPONSES = CYBER_DATA.get("responses", {})


# ---------------------------------------
# Chat Logic
# ---------------------------------------
def get_bot_response(message: str):
    msg = message.lower()

    # Exact match
    if msg in RESPONSES:
        return RESPONSES[msg]

    # Keyword match
    for key, value in RESPONSES.items():
        if key in msg:
            return value

    return (
        "I don't have information about that. Try asking about phishing, "
        "malware, ransomware, passwords, or other cyber security topics."
    )


# ---------------------------------------
# Request Model
# ---------------------------------------
class ChatRequest(BaseModel):
    message: str


# ---------------------------------------
# Routes
# ---------------------------------------
@app.get("/")
def home():
    return {"message": "Cyber Security Chatbot API running on Vercel!"}


@app.post("/chat")
def chat(request: ChatRequest):
    reply = get_bot_response(request.message)
    return {"user": request.message, "bot": reply}


# ---------------------------------------
# Vercel Handler
# ---------------------------------------
def handler(event, context):
    return app
