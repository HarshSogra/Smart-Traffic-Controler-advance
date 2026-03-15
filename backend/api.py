from fastapi import FastAPI
from pydantic import BaseModel

try:
    from model_loader import TrafficPredictor
except ModuleNotFoundError:
    from backend.model_loader import TrafficPredictor

app = FastAPI(title="Smart Traffic Prediction API")
predictor = TrafficPredictor()


class PredictionInput(BaseModel):
    vehicle_count: int
    avg_speed_kmh: int
    timestamp: str
    intersection_id: str
    weather: str
    signal_time_seconds: int


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict_traffic(data: PredictionInput):
    payload = data.model_dump()
    label = predictor.predict(payload)
    congestion = predictor.decode_congestion(label)

    return {
        "future_congestion_label": label,
        "future_congestion": congestion,
    }