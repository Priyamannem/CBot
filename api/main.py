from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load JSON data safely
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "cyber_data.json")

try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        CYBER_DATA = json.load(f)
except Exception as e:
    CYBER_DATA = {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Cyber Security Chatbot API is running successfully!"}

@app.post("/ask")
def ask_question(payload: dict):
    query = payload.get("query", "").lower()

    if not query:
        return {"answer": "Please ask a valid cyber security question."}

    # Find the best answer (simple matching)
    for item in CYBER_DATA.get("data", []):
        if item["question"].lower() in query:
            return {"answer": item["answer"]}

    return {"answer": "No exact match found. Please ask something related to cybersecurity."}

