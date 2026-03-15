import os

import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "dataset", "raw", "traffic_data.csv")
PROCESSED_PATH = os.path.join(PROJECT_ROOT, "dataset", "processed", "processed_data.csv")
ENCODER_PATH = os.path.join(PROJECT_ROOT, "backend", "models", "encoder.pkl")


def load_data():
    return pd.read_csv(DATA_PATH)


def handle_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    return df.drop(columns=["timestamp"])


def encode_categorical(df: pd.DataFrame):
    encoders = {}
    categorical_cols = ["intersection_id", "weather", "congestion_level"]

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df, encoders


def save_encoders(encoders):
    os.makedirs(os.path.dirname(ENCODER_PATH), exist_ok=True)
    joblib.dump(encoders, ENCODER_PATH)


def save_processed(df: pd.DataFrame):
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)


def main():
    print("Loading dataset...")
    df = load_data()

    print("Processing timestamps...")
    df = handle_timestamp(df)

    print("Encoding categorical features...")
    df, encoders = encode_categorical(df)

    print("Saving encoder...")
    save_encoders(encoders)

    print("Saving processed dataset...")
    save_processed(df)

    print("✅ Preprocessing completed!")


if __name__ == "__main__":
    main()