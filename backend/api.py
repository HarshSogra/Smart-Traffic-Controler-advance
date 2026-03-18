from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from model_loader import TrafficPredictor
except ModuleNotFoundError:
    from backend.model_loader import TrafficPredictor

app = FastAPI(title="Smart Traffic Prediction API")
predictor = TrafficPredictor()


# ---------------------- INPUT SCHEMA ----------------------
class PredictionInput(BaseModel):
    vehicle_count: int
    avg_speed_kmh: int | None = None
    avg_speed: int | None = None
    timestamp: str | None = None
    intersection_id: str | None = None
    weather: str | None = None
    signal_time_seconds: int | None = None
    temperature: float | None = None
    humidity: float | None = None


# ---------------------- WEATHER HELPERS ----------------------
def _infer_weather(temperature: float | None, humidity: float | None) -> str:
    default_weather = predictor.default_value("weather")

    if temperature is None or humidity is None:
        return default_weather

    if humidity >= 80:
        return "Rain"
    if humidity >= 60:
        return "Cloudy"
    if temperature >= 32:
        return "Clear"
    if temperature <= 12:
        return "Fog"

    return default_weather


def normalize_weather(weather: str) -> str:
    if not weather:
        return "Clear"

    weather = weather.capitalize()

    mapping = {
        "Sunny": "Clear",
        "Clear": "Clear",
        "Rainy": "Rain",
        "Rain": "Rain",
        "Cloudy": "Cloudy",
        "Foggy": "Fog",
        "Fog": "Fog"
    }

    return mapping.get(weather, "Clear")


# ---------------------- PAYLOAD NORMALIZATION ----------------------
def _normalize_payload(data: PredictionInput) -> dict:
    avg_speed_kmh = data.avg_speed_kmh if data.avg_speed_kmh is not None else data.avg_speed

    if avg_speed_kmh is None:
        raise HTTPException(
            status_code=422,
            detail="Provide avg_speed_kmh (or legacy avg_speed)."
        )

    timestamp = data.timestamp or datetime.utcnow().isoformat()
    intersection_id = data.intersection_id or predictor.default_value("intersection_id")

    # 🔥 FIXED WEATHER HANDLING
    raw_weather = data.weather or _infer_weather(data.temperature, data.humidity)
    weather = normalize_weather(raw_weather)

    signal_time_seconds = data.signal_time_seconds
    if signal_time_seconds is None:
        signal_time_seconds = max(20, min(120, int(30 + (data.vehicle_count * 0.7))))

    return {
        "vehicle_count": data.vehicle_count,
        "avg_speed_kmh": avg_speed_kmh,
        "timestamp": timestamp,
        "intersection_id": intersection_id,
        "weather": weather,
        "signal_time_seconds": signal_time_seconds,
    }


# ---------------------- ROUTES ----------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict_traffic(data: PredictionInput):
    try:
        payload = _normalize_payload(data)

        print("DEBUG PAYLOAD:", payload)  # helpful debug

        label = predictor.predict(payload)
        congestion = predictor.decode_congestion(label)

        return {
            "future_congestion_label": label,
            "future_congestion": congestion,
            "prediction": label,
        }

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/traffic-prediction")
def traffic_prediction_snapshot():
    now = datetime.utcnow().replace(microsecond=0).isoformat()
    intersections = predictor.get_allowed_values("intersection_id")[:5]
    weather = predictor.default_value("weather")

    predictions = []

    for idx, intersection in enumerate(intersections):
        payload = {
            "vehicle_count": 20 + (idx * 12),
            "avg_speed_kmh": 18 + (idx * 4),
            "timestamp": now,
            "intersection_id": intersection,
            "weather": weather,
            "signal_time_seconds": 35 + (idx * 8),
        }

        label = predictor.predict(payload)

        predictions.append(
            {
                "red_light": f"Red Light {chr(65 + idx)}",
                "intersection_id": intersection,
                "prediction": int(label),
                "future_congestion": predictor.decode_congestion(label),
            }
        )

    return {"predictions": predictions, "timestamp": now}