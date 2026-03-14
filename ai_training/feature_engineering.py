import pandas as pd
import joblib
import os

from sklearn.ensemble import IsolationForest

DATA_PATH = "../dataset/processed/processed_data.csv"
MODEL_PATH = "../backend/models/anomaly_model.pkl"


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def train_model(df):

    # remove label
    X = df.drop(columns=["congestion_level"])

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    return model


def save_model(model):
    os.makedirs("../backend/models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("✅ Anomaly model saved!")


def main():

    print("Loading dataset...")
    df = load_data()

    print("Training anomaly detection model...")
    model = train_model(df)

    save_model(model)


if __name__ == "__main__":
    main()