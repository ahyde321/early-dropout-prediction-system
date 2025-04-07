import os
import sys

# Get the absolute path of the project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from training.logreg_trainer import train_logistic_regression
from data.model_evaluator import evaluate_model

# Paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data/ready")

# ✅ Ensure required directories exist
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
X_train_path = os.path.join(DATA_DIR, "X_train.csv")
y_train_path = os.path.join(DATA_DIR, "y_train.csv")
X_val_path = os.path.join(DATA_DIR, "X_val.csv")
y_val_path = os.path.join(DATA_DIR, "y_val.csv")
model_path = os.path.join(MODEL_DIR, "logreg_model.pkl")

# ✅ Check required files
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    print(f"✅ Found file: {filepath}")

check_file_exists(X_train_path)
check_file_exists(y_train_path)

# 🚀 Train Logistic Regression model
print("🚀 Training Logistic Regression model with hyperparameter optimization...")
train_logistic_regression(
    X_train_path=X_train_path,
    y_train_path=y_train_path,
    model_path=model_path
)
print(f"✅ Model saved at {model_path}")

# ✅ Check model exists
check_file_exists(model_path)

# 📊 Evaluate on training set
print("📊 Evaluating on Training Data...")
evaluate_model(
    x_path=X_train_path,
    y_path=y_train_path,
    model_path=model_path
)

# ✅ Check validation data
check_file_exists(X_val_path)
check_file_exists(y_val_path)

# 📊 Evaluate on validation set
print("📊 Evaluating on Validation Data...")
evaluate_model(
    x_path=X_val_path,
    y_path=y_val_path,
    model_path=model_path
)

print("🎯 Logistic Regression Model Training & Evaluation Completed Successfully!")
