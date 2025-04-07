import os
import sys

# Set base path to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from training.xgboost_trainer import train_xgboost
from data.model_evaluator import evaluate_model

# Paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data", "ready")

# ✅ Ensure directories exist
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
X_train_path = os.path.join(DATA_DIR, "X_train.csv")
y_train_path = os.path.join(DATA_DIR, "y_train.csv")
X_val_path = os.path.join(DATA_DIR, "X_val.csv")
y_val_path = os.path.join(DATA_DIR, "y_val.csv")
model_path = os.path.join(MODEL_DIR, "xgboost_model.pkl")

# ✅ File existence check function
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    print(f"✅ Found file: {filepath}")

# ✅ Check training files
check_file_exists(X_train_path)
check_file_exists(y_train_path)

# 🚀 Train XGBoost model
print("🚀 Training XGBoost model with hyperparameter tuning...")
train_xgboost(
    X_train_path=X_train_path,
    y_train_path=y_train_path,
    model_path=model_path
)
print(f"✅ Model saved at {model_path}")

# ✅ Check model file
check_file_exists(model_path)

# 📊 Evaluate on training set
print("📊 Evaluating on Training Data...")
evaluate_model(
    x_path=X_train_path,
    y_path=y_train_path,
    model_path=model_path
)

# ✅ Check validation files
check_file_exists(X_val_path)
check_file_exists(y_val_path)

# 📊 Evaluate on validation set
print("📊 Evaluating on Validation Data...")
evaluate_model(
    x_path=X_val_path,
    y_path=y_val_path,
    model_path=model_path
)

print("🎯 XGBoost Model Training & Evaluation Completed Successfully!")
