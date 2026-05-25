from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Complaint(BaseModel):
    complaint: str

@app.get("/")
def home():
    return {"message": "Citizen Grievance API Running"}

@app.post("/predict")
def predict(data: Complaint):

    complaint_text = data.complaint

    return {
        "complaint_received": complaint_text,
        "department": "Water Department",
        "sentiment": "Critical",
        "priority_score": 0.91
    } 