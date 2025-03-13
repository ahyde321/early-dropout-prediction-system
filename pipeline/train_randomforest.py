import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, balanced_accuracy_score, roc_curve
from sklearn.model_selection import KFold, GridSearchCV
from utils.pred_utils import determine_optimal_threshold

# Define label mapping for string-based targets
LABEL_MAP = {"Likely Graduate": 0, "High Risk (Dropout)": 1}
REVERSE_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}

print("scikit-learn version:", sklearn.__version__)
print("joblib version:", joblib.__version__)

def train_random_forest(train_dataset_path, test_dataset_path, model_dir, validate_dataset_path=None, k_folds=5):
    """ Train, calibrate, and evaluate a Random Forest model for dropout prediction. """
    
    os.makedirs(model_dir, exist_ok=True)

    # --- Load datasets ---
    train_data = pd.read_csv(train_dataset_path)
    test_data = pd.read_csv(test_dataset_path)
    validate_data = pd.read_csv(validate_dataset_path) if validate_dataset_path and os.path.exists(validate_dataset_path) else None

    # --- Ensure 'Target' column exists ---
    for dataset, name in [(train_data, "training"), (test_data, "testing"), (validate_data, "validation")]:
        if dataset is not None and 'Target' not in dataset.columns:
            raise ValueError(f"The 'Target' column is missing in the {name} dataset.")

    # --- Convert categorical targets to numerical ---
    for dataset, name in [(train_data, "training"), (test_data, "testing"), (validate_data, "validation")]:
        if dataset is not None:
            if dataset['Target'].dtype == 'object':
                dataset['Target'] = dataset['Target'].map(LABEL_MAP)

            if dataset['Target'].isna().any():
                raise ValueError(f"Missing or invalid Target values found in the {name} dataset.")

    # --- Prepare Data Without SMOTE ---
    X_train, y_train = train_data.drop('Target', axis=1), train_data['Target']
    X_test, y_test = test_data.drop('Target', axis=1), test_data['Target']
    if validate_data is not None:
        X_validate, y_validate = validate_data.drop('Target', axis=1), validate_data['Target']

    # --- Save feature names ---
    joblib.dump(X_train.columns, os.path.join(model_dir, 'feature_names.joblib'))

    # --- Grid Search and Cross-Validation ---
    param_grid = {'n_estimators': [100, 200, 300], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5]}
    rf_model = RandomForestClassifier(random_state=42, class_weight={0: 1, 1: 6})  # Reduce dropout weight
    grid_search = GridSearchCV(rf_model, param_grid, cv=k_folds, scoring='accuracy', n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

    # --- Best model selection & calibration ---
    best_model = grid_search.best_estimator_
    print(f"\nBest Parameters: {grid_search.best_params_}")
    print(f"Best Cross-Validation Accuracy: {grid_search.best_score_:.4f}")

    calibrated_model = CalibratedClassifierCV(best_model, method='isotonic', cv='prefit')
    calibrated_model.fit(X_train, y_train)

    # --- Determine Optimal Threshold Using ROC Curve ---
    kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
    cross_val_probabilities, cross_val_labels = [], []
    for train_idx, val_idx in kf.split(X_train):
        X_kf_val, y_kf_val = X_train.iloc[val_idx], y_train.iloc[val_idx]
        y_kf_pred_prob = calibrated_model.predict_proba(X_kf_val)[:, 1]
        cross_val_probabilities.extend(y_kf_pred_prob)
        cross_val_labels.extend(y_kf_val)

    fpr, tpr, thresholds = roc_curve(cross_val_labels, cross_val_probabilities)
    optimal_idx = (tpr - fpr).argmax()
    optimal_threshold = max(min(thresholds[optimal_idx], 0.8), 0.5)

    print(f"\nAdjusted Optimal Threshold: {optimal_threshold:.2f}")

    # --- Save Model & Threshold ---
    joblib.dump(calibrated_model, os.path.join(model_dir, 'dropout_predictor_model.joblib'))
    joblib.dump(optimal_threshold, os.path.join(model_dir, 'optimal_threshold.joblib'))
    print("Model saved successfully.")
