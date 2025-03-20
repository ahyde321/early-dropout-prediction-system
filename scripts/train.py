import os
import sys

# Get the absolute path of the project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from utils.model_trainer import train_model
from utils.model_evaluator import evaluate_model

# Paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data/ready")

os.makedirs(MODEL_DIR, exist_ok=True)

# Train model
train_model(
    X_train_path=os.path.join(DATA_DIR, "X_train.csv"),
    y_train_path=os.path.join(DATA_DIR, "y_train.csv"),
    model_path=os.path.join(MODEL_DIR, "random_forest_model.pkl")
)

evaluate_model(
    x_val_path=os.path.join(DATA_DIR, "X_val.csv"),
    y_val_path=os.path.join(DATA_DIR, "y_val.csv"),
    model_path=os.path.join(MODEL_DIR, "random_forest_model.pkl")
)
