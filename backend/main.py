from fastapi import FastAPI, WebSocket
import asyncio
import random
import joblib
import os
import json
from agents.agent_manager import AI_Agents

app = FastAPI(title="SentimentBrand AI Backend")

# Load model if exists
MODEL_DIR = "ml_model"
model, vectorizer = None, None

def load_model():
    global model, vectorizer
    if os.path.exists(f"{MODEL_DIR}/sentiment_model.pkl") and os.path.exists(f"{MODEL_DIR}/vectorizer.pkl"):
        model = joblib.load(f"{MODEL_DIR}/sentiment_model.pkl")
        vectorizer = joblib.load(f"{MODEL_DIR}/vectorizer.pkl")

load_model()

@app.get("/")
def read_root():
    return {"message": "SentimentBrand AI API is running"}

@app.get("/predict")
def predict_sentiment(text: str):
    if not model or not vectorizer:
        return {"error": "Model not trained yet."}
    
    vec = vectorizer.transform([text.lower()])
    pred = model.predict(vec)[0]
    return {"text": text, "prediction": pred}

@app.websocket("/ws/livestream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Simulate an active data stream and Agent monitoring
    history = []
    
    try:
        while True:
            # Generate random synthetic incoming comment
            sample_texts = ["Great product!", "I hate the new UI.", "Standard delivery.", "Awful service today.", "Best experience ever."]
            text = random.choice(sample_texts)
            
            prediction = "neutral"
            if model and vectorizer:
                vec = vectorizer.transform([text.lower()])
                prediction = model.predict(vec)[0]
            
            data_point = {
                "text": text,
                "sentiment": prediction
            }
            history.append(data_point)
            if len(history) > 100:
                history.pop(0) # Keep last 100
                
            # Invoke Agents
            alerts = AI_Agents.monitoring_agent(history)
            decision = AI_Agents.decision_agent(history)
            
            payload = {
                "new_data": data_point,
                "alerts": alerts,
                "decision": decision
            }
            
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(2) # send new data every 2 seconds
            
    except Exception as e:
        print(f"Connection closed: {e}")
