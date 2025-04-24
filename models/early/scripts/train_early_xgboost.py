import os
import sys

# 📁 Set up path to early model root
EARLY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.abspath(os.path.join(EARLY_DIR, "..", "utils"))

# ➕ Append to sys.path for clean imports
if EARLY_DIR not in sys.path:
    sys.path.append(EARLY_DIR)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ✅ Import utilities and paths
from path_config import ARTIFACTS_DIR, READY_DIR
from training.xgboost_trainer import train_xgboost
from data.model_evaluator import evaluate_model

# ✅ Ensure required directories exist
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)

# 📄 Define file paths
X_train_path = os.path.join(READY_DIR, "X_train.csv")
y_train_path = os.path.join(READY_DIR, "y_train.csv")
X_val_path = os.path.join(READY_DIR, "X_val.csv")
y_val_path = os.path.join(READY_DIR, "y_val.csv")
model_path = os.path.join(ARTIFACTS_DIR, "xgboost_model.pkl")

# ✅ Utility to check files exist
def check_files_exist(file_paths):
    for filepath in file_paths:
        if not os.path.exists(filepath):
            print(f"❌ ERROR: File not found: {filepath}")
            sys.exit(1)
        print(f"✅ Found file: {filepath}")

# 🚦 Check data availability
check_files_exist([X_train_path, y_train_path])

# 🚀 Train XGBoost model with hyperparameter tuning
print("🚀 Training Early XGBoost model with hyperparameter tuning...")
train_xgboost(
    X_train_path=X_train_path,
    y_train_path=y_train_path,
    model_path=model_path
)
print(f"✅ Model saved at {model_path}")

# 🔍 Confirm model file
check_files_exist([model_path])

# 📊 Evaluate on training set
print("\n📊 Evaluating on Training Data...")
evaluate_model(
    x_path=X_train_path,
    y_path=y_train_path,
    model_path=model_path
)

# 📦 Check validation set
check_files_exist([X_val_path, y_val_path])

# 📊 Evaluate on validation set
print("\n📊 Evaluating on Validation Data...")
evaluate_model(
    x_path=X_val_path,
    y_path=y_val_path,
    model_path=model_path
)

print("\n🎯 Early XGBoost Model Training & Evaluation Completed Successfully!")
