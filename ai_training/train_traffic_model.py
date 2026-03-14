# ai_training/train_traffic_model.py

import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

DATA_PATH = "../dataset/processed/processed_data.csv"
MODEL_PATH = "../backend/models/traffic_model.pkl"


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def split_features_target(df):
    X = df.drop(columns=["congestion_level"])
    y = df["congestion_level"]
    return X, y


def train_model(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, predictions))
    print("\nClassification Report:\n")
    print(classification_report(y_test, predictions))


def save_model(model):
    os.makedirs("../backend/models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("✅ Model saved!")


def main():
    print("Loading processed data...")
    df = load_data()

    print("Splitting features and target...")
    X, y = split_features_target(df)

    print("Train-test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training model...")
    model = train_model(X_train, y_train)

    print("Evaluating model...")
    evaluate(model, X_test, y_test)

    save_model(model)


if __name__ == "__main__":
    main()