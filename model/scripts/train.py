import os
import sys

# Get the absolute path of the project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from utils.randomforest_trainer import train_random_forest
from utils.model_evaluator import evaluate_model

# Paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data/ready")

# ✅ Ensure required directories exist
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)  # In case the data directory is also missing

# File paths
X_train_path = os.path.join(DATA_DIR, "X_train.csv")
y_train_path = os.path.join(DATA_DIR, "y_train.csv")
X_val_path = os.path.join(DATA_DIR, "X_val.csv")
y_val_path = os.path.join(DATA_DIR, "y_val.csv")
model_path = os.path.join(MODEL_DIR, "random_forest_model.pkl")

# ✅ Function to check if required files exist before proceeding
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)  # Stop execution if a file is missing
    print(f"✅ Found file: {filepath}")

# Check if training data exists
check_file_exists(X_train_path)
check_file_exists(y_train_path)

# 🚀 Train model
print("🚀 Training Random Forest model...")
train_random_forest(
    X_train_path=X_train_path,
    y_train_path=y_train_path,
    model_path=model_path
)
print(f"✅ Model saved at {model_path}")

# ✅ Check if model exists before evaluation
check_file_exists(model_path)

# 📊 Evaluate on training set
print("📊 Evaluating on Training Data...")
evaluate_model(
    x_path=X_train_path,
    y_path=y_train_path,
    model_path=model_path
)

# ✅ Check if validation data exists before evaluating
check_file_exists(X_val_path)
check_file_exists(y_val_path)

# 📊 Evaluate on validation set
print("📊 Evaluating on Validation Data...")
evaluate_model(
    x_path=X_val_path,
    y_path=y_val_path,
    model_path=model_path
)

print("🎯 Model Training & Evaluation Completed Successfully!")
