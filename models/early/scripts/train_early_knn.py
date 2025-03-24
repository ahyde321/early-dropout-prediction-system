import os
import sys

# === Setup paths for early model ===
EARLY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.abspath(os.path.join(EARLY_DIR, "..", "utils"))

# Add paths for clean imports
if EARLY_DIR not in sys.path:
    sys.path.append(EARLY_DIR)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ✅ Import path constants and trainers
from path_config import READY_DIR, ARTIFACTS_DIR
from knn_trainer import train_optimized_knn
from model_evaluator import evaluate_model

# === Ensure required directories exist ===
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)

# === File paths ===
X_train_path = os.path.join(READY_DIR, "X_train.csv")
y_train_path = os.path.join(READY_DIR, "y_train.csv")
X_val_path = os.path.join(READY_DIR, "X_val.csv")
y_val_path = os.path.join(READY_DIR, "y_val.csv")
model_path = os.path.join(ARTIFACTS_DIR, "knn_model.pkl")

# ✅ File checker utility
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    print(f"✅ Found file: {filepath}")

# === Train KNN Model ===
check_file_exists(X_train_path)
check_file_exists(y_train_path)

print("🚀 Training KNN model (early) with hyperparameter optimization...")
train_optimized_knn(
    model_path=model_path,
    X_path=X_train_path,
    y_path=y_train_path
)
check_file_exists(model_path)
print(f"✅ Model saved at {model_path}")

# === Evaluate on Training Data ===
print("📊 Evaluating on Training Data...")
evaluate_model(
    x_path=X_train_path,
    y_path=y_train_path,
    model_path=model_path
)

# === Evaluate on Validation Data ===
check_file_exists(X_val_path)
check_file_exists(y_val_path)

print("📊 Evaluating on Validation Data...")
evaluate_model(
    x_path=X_val_path,
    y_path=y_val_path,
    model_path=model_path
)

print("🎯 Early KNN Model Training & Evaluation Completed Successfully!")
