import os
from datetime import datetime

import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "traffic_model_future.pkl")
ENCODER_PATH = os.path.join(MODELS_DIR, "encoder.pkl")


class TrafficPredictor:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.encoders = joblib.load(ENCODER_PATH)
        self.feature_order = list(self.model.feature_names_in_)

    def _encode_with_fallback(self, column: str, value: str) -> int:
        encoder = self.encoders[column]
        if value in encoder.classes_:
            return int(encoder.transform([value])[0])

        value_lower = value.lower()
        classes_lower = [cls.lower() for cls in encoder.classes_]
        if value_lower in classes_lower:
            idx = classes_lower.index(value_lower)
            return int(encoder.transform([encoder.classes_[idx]])[0])

        raise ValueError(
            f"Unknown value '{value}' for {column}. "
            f"Allowed values: {list(encoder.classes_)}"
        )

    def prepare_input(self, payload: dict) -> pd.DataFrame:
        timestamp = datetime.fromisoformat(payload["timestamp"])

        row = {
            "vehicle_count": payload["vehicle_count"],
            "avg_speed_kmh": payload["avg_speed_kmh"],
            "intersection_id": self._encode_with_fallback(
                "intersection_id", payload["intersection_id"]
            ),
            "weather": self._encode_with_fallback("weather", payload["weather"]),
            "signal_time_seconds": payload["signal_time_seconds"],
            "hour": timestamp.hour,
            "day_of_week": timestamp.weekday(),
            "is_weekend": 1 if timestamp.weekday() >= 5 else 0,
        }

        df = pd.DataFrame([row])
        return df.reindex(columns=self.feature_order)

    def predict(self, payload: dict) -> int:
        features = self.prepare_input(payload)
        prediction = self.model.predict(features)[0]
        return int(prediction)

    def decode_congestion(self, label: int) -> str:
        return str(self.encoders["congestion_level"].inverse_transform([label])[0])