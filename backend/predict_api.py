from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from model_loader import TrafficPredictor

app = FastAPI(title="Traffic Future Prediction API", version="1.0.0")
predictor = TrafficPredictor()


class PredictionInput(BaseModel):
    timestamp: str = Field(..., examples=["2024-01-01T08:30:00"])
    vehicle_count: int = Field(..., ge=0)
    avg_speed_kmh: float = Field(..., ge=0)
    intersection_id: str
    weather: str
    signal_time_seconds: int = Field(..., ge=0)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/schema")
def input_schema():
    return {
        "required_fields": [
            "timestamp",
            "vehicle_count",
            "avg_speed_kmh",
            "intersection_id",
            "weather",
            "signal_time_seconds",
        ],
        "intersection_id_allowed": predictor.get_allowed_values("intersection_id"),
        "weather_allowed": predictor.get_allowed_values("weather"),
    }


@app.post("/predict")
def predict(payload: PredictionInput):
    try:
        input_data = payload.model_dump()
        label_id = predictor.predict(input_data)
        return {
            "prediction": label_id,
            "prediction_label": predictor.decode_congestion(label_id),
            "input": input_data,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc
