import os
from utils.model_trainer import train_model, evaluate_model

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data/ready")

os.makedirs(MODEL_DIR, exist_ok=True)

# Train model
train_model(
    X_train_path=os.path.join(DATA_DIR, "X_train.csv"),
    y_train_path=os.path.join(DATA_DIR, "y_train.csv"),
    model_path=os.path.join(MODEL_DIR, "random_forest_model.pkl")
)

# Evaluate model
evaluate_model(
    model_path=os.path.join(MODEL_DIR, "random_forest_model.pkl"),
    X_path=os.path.join(DATA_DIR, "X_val.csv"),
    y_path=os.path.join(DATA_DIR, "y_val.csv")
)
