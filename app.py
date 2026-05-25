from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ---------------- CORS FIX ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- INPUT MODEL ----------------
class Complaint(BaseModel):
    text: str

# ---------------- SIMPLE PREDICTION LOGIC ----------------
def predict_department(text: str):
    text = text.lower()

    if "water" in text:
        return "Water Supply Department"
    elif "garbage" in text or "waste" in text:
        return "Municipality / Sanitation"
    elif "electricity" in text or "power" in text:
        return "Electricity Board"
    elif "road" in text or "street" in text:
        return "Public Works Department"
    else:
        return "General Grievance Department"


def predict_sentiment(text: str):
    text = text.lower()

    negative_words = ["not", "no", "bad", "problem", "issue", "delay", "dirty", "worst"]
    if any(word in text for word in negative_words):
        return "Negative"
    return "Neutral"


def predict_priority(text: str):
    text = text.lower()

    high_priority = ["no water", "no electricity", "accident", "danger", "urgent"]
    medium_priority = ["delay", "issue", "problem"]

    if any(word in text for word in high_priority):
        return 0.9
    elif any(word in text for word in medium_priority):
        return 0.6
    else:
        return 0.3


# ---------------- API ENDPOINT ----------------
@app.post("/predict")
def predict(data: Complaint):

    department = predict_department(data.text)
    sentiment = predict_sentiment(data.text)
    priority = predict_priority(data.text)

    return {
        "department": department,
        "sentiment": sentiment,
        "priority_score": priority
    }