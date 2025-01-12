import os
import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def validate_dropout_model(base_dir):
    """
    Validate a trained Random Forest model using the validation dataset.

    Args:
        base_dir (str): The base directory for input data and model files.

    Returns:
        None
    """
    validate_dataset_path = os.path.join(base_dir, 'data', 'validate_dataset.csv')
    model_path = os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.joblib')
    min_max_scaler_path = os.path.join(base_dir, 'models', 'min_max_scaler.joblib')
    feature_names_path = os.path.join(base_dir, 'models', 'feature_names.joblib')

    if not os.path.exists(validate_dataset_path):
        raise FileNotFoundError(f"Validation dataset not found at {validate_dataset_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler not found at {scaler_path}")
    if not os.path.exists(min_max_scaler_path):
        raise FileNotFoundError(f"Min-max scaler not found at {min_max_scaler_path}")
    if not os.path.exists(feature_names_path):
        raise FileNotFoundError(f"Feature names file not found at {feature_names_path}")

    data = pd.read_csv(validate_dataset_path)
    if 'Target' not in data.columns:
        raise ValueError("Validation dataset must contain a 'Target' column.")

    # Split features and target
    X_validate = data.drop('Target', axis=1)
    y_validate = data['Target']

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    min_max_scaler = joblib.load(min_max_scaler_path)
    feature_names = joblib.load(feature_names_path)

    # Scale validation data
    if 'Age at enrollment' in X_validate.columns:
        X_validate['Age at enrollment'] = min_max_scaler.transform(X_validate[['Age at enrollment']])

    numerical_columns = joblib.load(os.path.join(base_dir, 'models', 'numerical_columns.joblib'))
    X_validate[numerical_columns] = scaler.transform(X_validate[numerical_columns])

    # Ensure feature order matches the trained model
    X_validate = X_validate[feature_names]

    # Make predictions
    y_pred = model.predict(X_validate)

    # Evaluate the model
    print("Validation Results:")
    print("Accuracy:", accuracy_score(y_validate, y_pred))
    print("\nClassification Report:\n", classification_report(y_validate, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_validate, y_pred))