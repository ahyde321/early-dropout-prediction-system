import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def train_knn_with_kfold(train_path, validate_path, test_path, model_dir, n_neighbors=5):
    """
    Train and evaluate a KNN model using the training, validation, and test datasets.

    Args:
        train_path (str): Path to the training dataset.
        validate_path (str): Path to the validation dataset.
        test_path (str): Path to the test dataset.
        model_dir (str): Directory to save trained models and metadata.
        n_neighbors (int): Number of neighbors for the KNN algorithm.

    Returns:
        None
    """
    # Ensure the model directory exists
    os.makedirs(model_dir, exist_ok=True)

    # Load the datasets
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training dataset not found at {train_path}")
    if not os.path.exists(validate_path):
        raise FileNotFoundError(f"Validation dataset not found at {validate_path}")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Test dataset not found at {test_path}")

    train_data = pd.read_csv(train_path)
    validate_data = pd.read_csv(validate_path)
    test_data = pd.read_csv(test_path)

    # Ensure the datasets have the 'Target' column
    if 'Target' not in train_data.columns or 'Target' not in validate_data.columns or 'Target' not in test_data.columns:
        raise ValueError("All datasets must contain a 'Target' column.")

    # Split into features (X) and targets (y)
    X_train, y_train = train_data.drop('Target', axis=1), train_data['Target']
    X_validate, y_validate = validate_data.drop('Target', axis=1), validate_data['Target']
    X_test, y_test = test_data.drop('Target', axis=1), test_data['Target']

    # Save feature names for interpretability
    feature_names = X_train.columns
    joblib.dump(feature_names, os.path.join(model_dir, 'feature_names.joblib'))

    # Train KNN on the training data
    print("\nTraining KNN model on the training dataset...")
    knn_model = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn_model.fit(X_train, y_train)

    # Evaluate on the validation dataset
    print("\nEvaluating on the validation dataset...")
    validate_predictions = knn_model.predict(X_validate)
    validate_accuracy = accuracy_score(y_validate, validate_predictions)
    print(f"Validation Accuracy: {validate_accuracy:.4f}")
    print("\nValidation Classification Report:\n", classification_report(y_validate, validate_predictions))
    print("\nValidation Confusion Matrix:\n", confusion_matrix(y_validate, validate_predictions))

    # Final evaluation on the test dataset
    print("\nEvaluating on the test dataset...")
    test_predictions = knn_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_predictions)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print("\nTest Classification Report:\n", classification_report(y_test, test_predictions))
    print("\nTest Confusion Matrix:\n", confusion_matrix(y_test, test_predictions))

    # Save the final KNN model
    joblib.dump(knn_model, os.path.join(model_dir, 'knn_model.joblib'))
    print("Final KNN model saved.")

# Example usage
if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.dirname(__file__))
    train_path = os.path.join(base_dir, 'data', 'processed', 'train_dataset.csv')
    validate_path = os.path.join(base_dir, 'data', 'processed', 'validate_dataset.csv')
    test_path = os.path.join(base_dir, 'data', 'processed', 'test_dataset.csv')
    model_dir = os.path.join(base_dir, 'models', 'knn')

    train_knn_with_kfold(train_path, validate_path, test_path, model_dir, n_neighbors=5)
