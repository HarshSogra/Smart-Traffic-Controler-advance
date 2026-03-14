
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

DATA_PATH = "../dataset/raw/traffic_data.csv"
PROCESSED_PATH = "../dataset/processed/processed_data.csv"
ENCODER_PATH = "../backend/models/encoder.pkl"


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def handle_timestamp(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

    df.drop(columns=["timestamp"], inplace=True)
    return df


def encode_categorical(df):
    encoders = {}

    categorical_cols = ["intersection_id", "weather", "congestion_level"]

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df, encoders


def save_encoders(encoders):
    os.makedirs("../backend/models", exist_ok=True)
    joblib.dump(encoders, ENCODER_PATH)


def save_processed(df):
    os.makedirs("../dataset/processed", exist_ok=True)
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