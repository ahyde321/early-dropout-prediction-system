import os
import sys

# 🔧 Set up path to access `path_config.py` and `utils/`
EARLY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.abspath(os.path.join(EARLY_DIR, "..", "utils"))

# Add paths to sys.path for clean imports
if EARLY_DIR not in sys.path:
    sys.path.append(EARLY_DIR)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ✅ Import from early model's path config and shared utils
from path_config import READY_DIR, ARTIFACTS_DIR
from training.randomforest_trainer import train_random_forest
from data.model_evaluator import evaluate_model

# === Ensure required directories exist ===
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)

# === File paths ===
X_train_path = os.path.join(READY_DIR, "X_train.csv")
y_train_path = os.path.join(READY_DIR, "y_train.csv")
X_val_path = os.path.join(READY_DIR, "X_val.csv")
y_val_path = os.path.join(READY_DIR, "y_val.csv")
model_path = os.path.join(ARTIFACTS_DIR, "random_forest_model.pkl")

# === File checker utility ===
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    print(f"✅ Found file: {filepath}")

# === Train Random Forest ===
check_file_exists(X_train_path)
check_file_exists(y_train_path)

print("🚀 Training Random Forest model (early)...")
train_random_forest(
    X_train_path=X_train_path,
    y_train_path=y_train_path,
    model_path=model_path
)
check_file_exists(model_path)

# === Evaluate on training data ===
print("📊 Evaluating on Training Data...")
evaluate_model(
    x_path=X_train_path,
    y_path=y_train_path,
    model_path=model_path
)

# === Evaluate on validation data ===
check_file_exists(X_val_path)
check_file_exists(y_val_path)

print("📊 Evaluating on Validation Data...")
evaluate_model(
    x_path=X_val_path,
    y_path=y_val_path,
    model_path=model_path
)

print("🎯 Early Model Training & Evaluation Completed Successfully!")
