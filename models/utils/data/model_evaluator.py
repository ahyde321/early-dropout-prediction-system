import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

def evaluate_model(model_path, x_path, y_path):
    """
    Evaluates a trained model using multiple performance metrics.
    """
    # Load data
    X = pd.read_csv(x_path)
    y = pd.read_csv(y_path).values.ravel()

    # Load model
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Make predictions
    y_pred = model.predict(X)

    # Calculate metrics
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average="weighted")  # Change to "macro" if needed
    recall = recall_score(y, y_pred, average="weighted")
    f1 = f1_score(y, y_pred, average="weighted")

    # Display results
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("\nClassification Report:\n", classification_report(y, y_pred))
    
    # Display confusion matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(y, y_pred))

    return accuracy, precision, recall, f1
