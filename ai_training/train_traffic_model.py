# ai_training/train_traffic_model_future.py

import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Paths
DATA_PATH = "../dataset/processed/processed_data.csv"
MODEL_PATH = "../backend/models/traffic_model_future.pkl"


# ------------------------
# Load dataset
# ------------------------
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


# ------------------------
# Prepare features and target for future prediction
# ------------------------
def prepare_future_target(df, future_steps=20):
    """
    future_steps: number of rows to shift to predict future congestion
                  e.g., 20 steps ~ 5 minutes into the future
    """
    print(f"Shifting target by {future_steps} rows (~5 minutes ahead)")

    df['future_congestion'] = df['congestion_level'].shift(-future_steps)

    # Drop rows with NaN target
    df = df.dropna(subset=['future_congestion'])

    X = df.drop(columns=['congestion_level', 'future_congestion'])
    y = df['future_congestion']

    return X, y


# ------------------------
# Train the model
# ------------------------
def train_model(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model


# ------------------------
# Evaluate the model
# ------------------------
def evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)
    print("\nAccuracy:", accuracy_score(y_test, predictions))
    print("\nClassification Report:\n")
    print(classification_report(y_test, predictions))


# ------------------------
# Save the trained model
# ------------------------
def save_model(model):
    os.makedirs("../backend/models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("✅ 5-minute future traffic model saved!")


# ------------------------
# Main
# ------------------------
def main():
    print("Loading processed data...")
    df = load_data()

    print("Preparing features and future target...")
    X, y = prepare_future_target(df, future_steps=20)

    print("Train-test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training model for 5-min future prediction...")
    model = train_model(X_train, y_train)

    print("Evaluating model...")
    evaluate(model, X_test, y_test)

    save_model(model)


if __name__ == "__main__":
    main()