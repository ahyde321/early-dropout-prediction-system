import os
import sys

# 🔧 Set up paths
FINAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.abspath(os.path.join(FINAL_DIR, "..", "utils"))

# Add to sys.path for clean imports
if FINAL_DIR not in sys.path:
    sys.path.append(FINAL_DIR)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ✅ Imports
from path_config import READY_DIR, ARTIFACTS_DIR
from training.logreg_trainer import train_logistic_regression
from data.model_evaluator import evaluate_model

# === Ensure output directories exist ===
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)

# === Define file paths ===
X_train_path = os.path.join(READY_DIR, "X_train.csv")
y_train_path = os.path.join(READY_DIR, "y_train.csv")
X_val_path = os.path.join(READY_DIR, "X_val.csv")
y_val_path = os.path.join(READY_DIR, "y_val.csv")
model_path = os.path.join(ARTIFACTS_DIR, "logreg_model.pkl")

# === File check utility ===
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    print(f"✅ Found: {filepath}")

# === Check all required files ===
for path in [X_train_path, y_train_path, X_val_path, y_val_path]:
    check_file_exists(path)

# === Train Logistic Regression Model ===
print("\n🚀 Training Logistic Regression model (final) with hyperparameter optimization...\n")
train_result = train_logistic_regression(
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

print("\n🎯 Final Logistic Regression Model Training & Evaluation Completed Successfully!")
