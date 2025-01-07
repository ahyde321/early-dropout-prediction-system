import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os
import joblib

def train_dropout_model(dataset_path, model_dir):
    """
    Train a Random Forest model for student dropout prediction, scale numerical features, 
    and save the trained model, scalers, and feature metadata.

    Args:
        dataset_path (str): The file path to the preprocessed dataset CSV.
        model_dir (str): Directory to save the trained model and scalers.

    Returns:
        None
    """
    # Ensure model directory exists
    os.makedirs(model_dir, exist_ok=True)

    # Load the dataset
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    
    data = pd.read_csv(dataset_path)

    # Split the data into features (X) and target (y)
    if 'Target' not in data.columns:
        raise ValueError("Dataset must contain a 'Target' column.")
    
    X = data.drop('Target', axis=1)
    y = data['Target']

    # Define numerical columns
    numerical_columns = ['Age at enrollment', 'Curricular units 1st sem (credited)',
                         'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (evaluations)',
                         'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)',
                         'Curricular units 1st sem (without evaluations)', 'Curricular units 2nd sem (credited)',
                         'Curricular units 2nd sem (enrolled)', 'Curricular units 2nd sem (evaluations)',
                         'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)',
                         'Curricular units 2nd sem (without evaluations)']

    # Split the dataset into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize scalers
    min_max_scaler = MinMaxScaler()
    scaler = StandardScaler()

    # Apply MinMax scaling to 'Age at enrollment'
    if 'Age at enrollment' in X_train.columns:
        X_train[['Age at enrollment']] = min_max_scaler.fit_transform(X_train[['Age at enrollment']])
        X_test[['Age at enrollment']] = min_max_scaler.transform(X_test[['Age at enrollment']])

    # Apply Standard scaling to other numerical columns
    X_train[numerical_columns] = scaler.fit_transform(X_train[numerical_columns])
    X_test[numerical_columns] = scaler.transform(X_test[numerical_columns])

    # Save feature names for interpretability
    feature_names = X_train.columns
    joblib.dump(feature_names, os.path.join(model_dir, 'feature_names.joblib'))

    # Choose and train the model (Random Forest)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Feature Importance (For interpretability in Random Forests)
    feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\nFeature Importances:\n", feature_importances.head(10))

    # Save the model and scalers
    joblib.dump(model, os.path.join(model_dir, 'dropout_predictor_model.joblib'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.joblib'))
    joblib.dump(min_max_scaler, os.path.join(model_dir, 'min_max_scaler.joblib'))
    joblib.dump(numerical_columns, os.path.join(model_dir, 'numerical_columns.joblib'))

    print("Model and scalers saved successfully.")
