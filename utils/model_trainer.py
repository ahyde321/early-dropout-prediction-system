import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def train_model(X_train_path, y_train_path, model_path):
    """
    Trains a Random Forest classifier and saves the model.
    """
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).values.ravel()

    model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"✅ Model trained and saved at: {model_path}")

def evaluate_model(model_path, X_path, y_path):
    """
    Evaluates a trained model.
    """
    X = pd.read_csv(X_path)
    y = pd.read_csv(y_path).values.ravel()

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    y_pred = model.predict(X)
    accuracy = (y_pred == y).mean()
    print(f"📊 Accuracy: {accuracy:.4f}")
