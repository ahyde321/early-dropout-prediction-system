import os
import sys

# 🔧 Set up path to access `path_config.py` and `utils/`
FINAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.abspath(os.path.join(FINAL_DIR, "..", "utils"))

# Add paths to sys.path for clean imports
if FINAL_DIR not in sys.path:
    sys.path.append(FINAL_DIR)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ✅ Import path constants and utilities
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

# ✅ File checker
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    print(f"✅ Found file: {filepath}")

# ✅ Check all required files
for path in [X_train_path, y_train_path, X_val_path, y_val_path]:
    check_file_exists(path)

# === Train Random Forest Model ===
print("🚀 Training Random Forest model (final) with hyperparameter optimization...")
train_result = train_random_forest(
    X_train_path=X_train_path,
    y_train_path=y_train_path,
    model_path=model_path,
    optimize=True,
    search_type="random",
    n_iter=30,
    cv=5,
    early_stop_cv_score_threshold=0.7
)

check_file_exists(model_path)
print(f"✅ Model saved at {model_path}")
print(f"🔧 Hyperparameters used: {train_result['best_params']}")
print(f"🎯 Optimal threshold for F1: {train_result['threshold']:.3f}")

# === Evaluate on Training Data ===
print("\n📊 Evaluating on Training Data...")
evaluate_model(
    x_path=X_train_path,
    y_path=y_train_path,
    model_path=model_path
)

# === Evaluate on Validation Data ===
print("\n📊 Evaluating on Validation Data...")
evaluate_model(
    x_path=X_val_path,
    y_path=y_val_path,
    model_path=model_path
)

print("\n🎯 Final Random Forest Model Training & Evaluation Completed Successfully!")
