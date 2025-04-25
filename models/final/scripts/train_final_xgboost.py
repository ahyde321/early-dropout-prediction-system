import os
import sys

# 🔧 Set up paths for `path_config.py` and shared `utils`
FINAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.abspath(os.path.join(FINAL_DIR, "..", "utils"))

if FINAL_DIR not in sys.path:
    sys.path.append(FINAL_DIR)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ✅ Import constants and utilities
from path_config import READY_DIR, ARTIFACTS_DIR
from training.xgboost_trainer import train_xgboost
from data.model_evaluator import evaluate_model

# === Ensure necessary directories exist ===
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)

# === Define file paths ===
X_train_path = os.path.join(READY_DIR, "X_train.csv")
y_train_path = os.path.join(READY_DIR, "y_train.csv")
X_val_path = os.path.join(READY_DIR, "X_val.csv")
y_val_path = os.path.join(READY_DIR, "y_val.csv")
model_path = os.path.join(ARTIFACTS_DIR, "xgboost_model.pkl")

# === File checker ===
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    print(f"✅ Found: {filepath}")

# === Verify all necessary files ===
for path in [X_train_path, y_train_path, X_val_path, y_val_path]:
    check_file_exists(path)

# === Train XGBoost ===
print("\n🚀 Training XGBoost model (final) with hyperparameter tuning...\n")
train_result = train_xgboost(
    X_train_path=X_train_path,
    y_train_path=y_train_path,
    model_path=model_path
)

print(f"✅ Model saved at: {model_path}")
if isinstance(train_result, dict) and 'best_params' in train_result:
    print(f"🔧 Best hyperparameters: {train_result['best_params']}")

# === Evaluate on Training Data ===
print("\n📊 Evaluation on Training Data:")
evaluate_model(
    x_path=X_train_path,
    y_path=y_train_path,
    model_path=model_path
)

# === Evaluate on Validation Data ===
print("\n📊 Evaluation on Validation Data:")
evaluate_model(
    x_path=X_val_path,
    y_path=y_val_path,
    model_path=model_path
)

print("\n🎯 Final XGBoost Model Training & Evaluation Completed Successfully!")
