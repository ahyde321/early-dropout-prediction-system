import os
import sys

# 🔧 Set up paths to access `path_config.py` and `utils/`
FINAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.abspath(os.path.join(FINAL_DIR, "..", "utils"))

# Add clean import paths
if FINAL_DIR not in sys.path:
    sys.path.append(FINAL_DIR)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ✅ Imports
from path_config import READY_DIR, ARTIFACTS_DIR
from training.knn_trainer import train_optimized_knn
from data.model_evaluator import evaluate_model

# === Ensure required directories exist ===
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)

# === File paths ===
X_train_path = os.path.join(READY_DIR, "X_train.csv")
y_train_path = os.path.join(READY_DIR, "y_train.csv")
X_val_path = os.path.join(READY_DIR, "X_val.csv")
y_val_path = os.path.join(READY_DIR, "y_val.csv")
model_path = os.path.join(ARTIFACTS_DIR, "knn_model.pkl")

# === File checker ===
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    print(f"✅ Found: {filepath}")

# ✅ Verify all required files
for file in [X_train_path, y_train_path, X_val_path, y_val_path]:
    check_file_exists(file)

# === Train KNN Model ===
print("\n🚀 Training KNN model (final) with hyperparameter optimization...\n")
train_result = train_optimized_knn(
    model_path=model_path,
    X_path=X_train_path,
    y_path=y_train_path
)

print(f"\n✅ Model saved at: {model_path}")
print(f"🔧 Best hyperparameters: {train_result.get('best_params', 'N/A')}")

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

print("\n🎯 Final KNN Model Training & Evaluation Completed Successfully!")
