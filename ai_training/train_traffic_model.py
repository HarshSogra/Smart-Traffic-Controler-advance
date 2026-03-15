import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "dataset", "processed", "processed_data.csv")
MODEL_PATH = os.path.join(PROJECT_ROOT, "backend", "models", "traffic_model_future.pkl")


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def prepare_future_target(df: pd.DataFrame, future_steps: int = 1):
    """
    future_steps: number of rows to shift to predict future congestion.
                  e.g., 1 row ahead ~ 5 minutes for this dataset.
    """
    df = df.copy()
    df["future_congestion"] = df["congestion_level"].shift(-future_steps)
    df = df.dropna(subset=["future_congestion"])

    X = df.drop(columns=["congestion_level", "future_congestion"])
    y = df["future_congestion"].astype(int)
    return X, y


def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)
    print("\nAccuracy:", accuracy_score(y_test, predictions))
    print("\nClassification Report:\n")
    print(classification_report(y_test, predictions))


def save_model(model):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Future traffic model saved: {MODEL_PATH}")


def main():
    print("Loading processed data...")
    df = load_data()

    print("Preparing features and future target...")
    X, y = prepare_future_target(df, future_steps=1)

    print("Train-test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training model for future prediction...")
    model = train_model(X_train, y_train)

    print("Evaluating model...")
    evaluate(model, X_test, y_test)

    save_model(model)


if __name__ == "__main__":
    main()