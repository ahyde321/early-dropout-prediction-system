import os
import sys
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    auc
)

# === Setup: Add early and utils to path ===
EARLY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.abspath(os.path.join(EARLY_DIR, "..", "utils"))

if EARLY_DIR not in sys.path:
    sys.path.append(EARLY_DIR)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ✅ Import early model paths
from path_config import ARTIFACTS_DIR, READY_DIR

# === Load model & test data ===
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "random_forest_model.pkl")
X_TEST_PATH = os.path.join(READY_DIR, "X_test.csv")
Y_TEST_PATH = os.path.join(READY_DIR, "y_test.csv")

# --- Load model ---
model = joblib.load(MODEL_PATH)

# --- Load test data ---
X_test = pd.read_csv(X_TEST_PATH)
y_test = pd.read_csv(Y_TEST_PATH)

# ---- Make predictions ----
y_pred = model.predict(X_test)

# ---- Try to get prediction probabilities ----
try:
    y_proba = model.predict_proba(X_test)[:, 1]
    proba_available = True
except AttributeError:
    y_proba = None
    proba_available = False

# ---- Evaluation metrics ----
print("📊 Evaluation Metrics (Early RF Model):")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
print("\n📄 Classification Report:\n", classification_report(y_test, y_pred))
print("🧮 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ---- Optional: Plot ROC Curve ----
if proba_available and len(np.unique(y_test)) == 2:
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic - Early RF Model')
    plt.legend(loc="lower right")
    plt.grid()
    plt.show()
else:
    print("⚠️ ROC curve not plotted (predict_proba not available or not binary classification).")
