import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score, KFold
import os
import joblib

def train_random_forest(train_dataset_path, test_dataset_path, model_dir, validate_dataset_path=None, k_folds=5):
    """
    Train a Random Forest model for student dropout prediction using pre-partitioned datasets,
    perform K-Fold Cross-Validation, and save the trained model and feature metadata.

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

    if not os.path.exists(train_dataset_path):
        raise FileNotFoundError(f"Training dataset not found at {train_dataset_path}")
    if not os.path.exists(test_dataset_path):
        raise FileNotFoundError(f"Testing dataset not found at {test_dataset_path}")
    
    train_data = pd.read_csv(train_dataset_path)
    test_data = pd.read_csv(test_dataset_path)
    
    if validate_dataset_path:
        if not os.path.exists(validate_dataset_path):
            raise FileNotFoundError(f"Validation dataset not found at {validate_dataset_path}")
        validate_data = pd.read_csv(validate_dataset_path)
    else:
        validate_data = None

    # Split features (X) and target (y) for training and testing
    if 'Target' not in train_data.columns or 'Target' not in test_data.columns:
        raise ValueError("Datasets must contain a 'Target' column.")
    
    X_train, y_train = train_data.drop('Target', axis=1), train_data['Target']
    X_test, y_test = test_data.drop('Target', axis=1), test_data['Target']

    # Handle validation dataset if provided
    if validate_data is not None:
        if 'Target' not in validate_data.columns:
            raise ValueError("Validation dataset must contain a 'Target' column.")
        X_validate, y_validate = validate_data.drop('Target', axis=1), validate_data['Target']

    # Save feature names for interpretability
    feature_names = X_train.columns
    joblib.dump(feature_names, os.path.join(model_dir, 'feature_names.joblib'))

    # Perform K-Fold Cross-Validation
    print(f"\nPerforming {k_folds}-Fold Cross-Validation...")
    rf_model = RandomForestClassifier(random_state=42)
    kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
    cross_val_scores = []

    for train_index, val_index in kf.split(X_train):
        X_kf_train, X_kf_val = X_train.iloc[train_index], X_train.iloc[val_index]
        y_kf_train, y_kf_val = y_train.iloc[train_index], y_train.iloc[val_index]

        rf_model.fit(X_kf_train, y_kf_train)
        score = rf_model.score(X_kf_val, y_kf_val)
        cross_val_scores.append(score)
        print(f"Fold Accuracy: {score:.4f}")

    mean_accuracy = sum(cross_val_scores) / len(cross_val_scores)
    print(f"\nCross-Validation Accuracy Scores: {cross_val_scores}")
    print(f"Mean Cross-Validation Accuracy: {mean_accuracy:.4f}")

    # Train the final model on the entire training dataset
    print("\nTraining the final model on the entire training dataset...")
    rf_model.fit(X_train, y_train)

    print(f"Final model trained with n_estimators=200.")

    # Evaluate on validation set if provided
    if validate_data is not None:
        print("\nValidating the model...")
        y_validate_pred = rf_model.predict(X_validate)
        print("Validation Accuracy:", accuracy_score(y_validate, y_validate_pred))
        print("\nValidation Classification Report:\n", classification_report(y_validate, y_validate_pred))
        print("\nValidation Confusion Matrix:\n", confusion_matrix(y_validate, y_validate_pred))

    # Evaluate on test set
    print("\nTesting the model...")
    y_test_pred = rf_model.predict(X_test)
    print("Test Accuracy:", accuracy_score(y_test, y_test_pred))
    print("\nTest Classification Report:\n", classification_report(y_test, y_test_pred))
    print("\nTest Confusion Matrix:\n", confusion_matrix(y_test, y_test_pred))

    # Feature Importance (For interpretability in Random Forests)
    feature_importances = pd.Series(rf_model.feature_importances_, index=feature_names).sort_values(ascending=False)
    print("\nFeature Importances:\n", feature_importances.head(10))

    # Save the model
    joblib.dump(rf_model, os.path.join(model_dir, 'dropout_predictor_model.joblib'))

    print("Model saved successfully.")
