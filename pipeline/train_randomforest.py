import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import KFold, GridSearchCV
from utils.pred_utils import determine_optimal_threshold

# Define label mapping for string-based targets (if applicable)
LABEL_MAP = {"Likely Graduate": 0, "High Risk (Dropout)": 1}
REVERSE_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}

def train_random_forest(train_dataset_path, test_dataset_path, model_dir, validate_dataset_path=None, k_folds=5):
    """
    Train a Random Forest model for student dropout prediction using pre-partitioned datasets,
    perform Grid Search with K-Fold Cross-Validation, and save the trained model and feature metadata.

    Args:
        train_dataset_path (str): The file path to the preprocessed training dataset CSV.
        test_dataset_path (str): The file path to the preprocessed testing dataset CSV.
        model_dir (str): Directory to save the trained model and metadata.
        validate_dataset_path (str, optional): The file path to the preprocessed validation dataset CSV.
        k_folds (int): Number of folds for K-Fold Cross-Validation.

    Returns:
        None
    """
    os.makedirs(model_dir, exist_ok=True)

    # Load datasets and check for existence
    if not os.path.exists(train_dataset_path):
        raise FileNotFoundError(f"Training dataset not found at {train_dataset_path}")
    if not os.path.exists(test_dataset_path):
        raise FileNotFoundError(f"Testing dataset not found at {test_dataset_path}")

    train_data = pd.read_csv(train_dataset_path)
    test_data = pd.read_csv(test_dataset_path)

    if validate_dataset_path and os.path.exists(validate_dataset_path):
        validate_data = pd.read_csv(validate_dataset_path)
    else:
        validate_data = None

    # Ensure 'Target' column exists and convert it to integers
    if 'Target' not in train_data.columns or 'Target' not in test_data.columns:
        raise ValueError("Datasets must contain a 'Target' column.")

    # Convert target labels (string-based or numeric) to integers
    if train_data['Target'].dtype == 'object':
        train_data['Target'] = train_data['Target'].map(LABEL_MAP)
    if test_data['Target'].dtype == 'object':
        test_data['Target'] = test_data['Target'].map(LABEL_MAP)
    if validate_data is not None and validate_data['Target'].dtype == 'object':
        validate_data['Target'] = validate_data['Target'].map(LABEL_MAP)

    # Split features and target
    X_train, y_train = train_data.drop('Target', axis=1), train_data['Target'].astype(int)
    X_test, y_test = test_data.drop('Target', axis=1), test_data['Target'].astype(int)

    if validate_data is not None:
        if 'Target' not in validate_data.columns:
            raise ValueError("Validation dataset must contain a 'Target' column.")
        X_validate, y_validate = validate_data.drop('Target', axis=1), validate_data['Target'].astype(int)

    # Save feature names for later use
    feature_names = X_train.columns
    joblib.dump(feature_names, os.path.join(model_dir, 'feature_names.joblib'))

    # Define parameter grid for Grid Search
    param_grid = {
        'n_estimators': [50, 100, 200, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }

    # Perform Grid Search with Cross-Validation
    print("\nStarting Grid Search with Cross-Validation...")
    rf_model = RandomForestClassifier(random_state=42, class_weight='balanced')
    grid_search = GridSearchCV(
        estimator=rf_model,
        param_grid=param_grid,
        cv=k_folds,
        scoring='accuracy',
        n_jobs=-1,
        verbose=2
    )

    grid_search.fit(X_train, y_train)

    # Get the best parameters and model
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_
    print("\n=== Grid Search Results ===")
    print(f"Best Parameters: {best_params}")
    print(f"Best Cross-Validation Accuracy: {grid_search.best_score_:.4f}")

    # Final model training
    best_model.fit(X_train, y_train)

    # Determine the optimal threshold using precision-recall curve
    kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
    cross_val_probabilities, cross_val_labels = [], []

    # Perform K-Fold cross-validation to gather probabilities for threshold determination
    for train_index, val_index in kf.split(X_train):
        X_kf_train, X_kf_val = X_train.iloc[train_index], X_train.iloc[val_index]
        y_kf_train, y_kf_val = y_train.iloc[train_index], y_train.iloc[val_index]

        best_model.fit(X_kf_train, y_kf_train)
        y_kf_pred_prob = best_model.predict_proba(X_kf_val)[:, 1]
        cross_val_probabilities.extend(y_kf_pred_prob)
        cross_val_labels.extend(y_kf_val)

    # Calculate optimal threshold based on cross-validation data
    optimal_threshold = determine_optimal_threshold(cross_val_probabilities, cross_val_labels, plot=True)
    print(f"\nOptimal Threshold from Cross-Validation: {optimal_threshold:.2f}")

    # Evaluate on validation set if provided
    if validate_data is not None:
        print("\nValidating the model...")
        y_validate_pred_prob = best_model.predict_proba(X_validate)[:, 1]
        y_validate_pred = (y_validate_pred_prob > optimal_threshold).astype(int)
        print("Validation Accuracy:", accuracy_score(y_validate, y_validate_pred))
        print("\nValidation Classification Report:\n", classification_report(y_validate, y_validate_pred, target_names=["Likely Graduate", "High Risk (Dropout)"]))
        print("\nValidation Confusion Matrix:\n", confusion_matrix(y_validate, y_validate_pred))

    # Evaluate on test set
    print("\nTesting the model...")
    y_test_pred_prob = best_model.predict_proba(X_test)[:, 1]
    y_test_pred = (y_test_pred_prob > optimal_threshold).astype(int)
    print("Test Accuracy:", accuracy_score(y_test, y_test_pred))
    print("\nTest Classification Report:\n", classification_report(y_test, y_test_pred, target_names=["Likely Graduate", "High Risk (Dropout)"]))
    print("\nTest Confusion Matrix:\n", confusion_matrix(y_test, y_test_pred))

    # Save the model
    joblib.dump(best_model, os.path.join(model_dir, 'dropout_predictor_model.joblib'))
    print("Model saved successfully.")
