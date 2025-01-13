import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
import joblib

def train_logistic_regression(train_path, validate_path, test_path, model_dir):
    """
    Train and evaluate a Logistic Regression model for dropout prediction with hyperparameter tuning using GridSearchCV.

    Args:
        train_path (str): Path to the training dataset.
        validate_path (str): Path to the validation dataset.
        test_path (str): Path to the testing dataset.
        model_dir (str): Directory to save the trained model.
    """
    # Ensure the model directory exists
    os.makedirs(model_dir, exist_ok=True)

    # Load datasets
    train_data = pd.read_csv(train_path)
    validate_data = pd.read_csv(validate_path)
    test_data = pd.read_csv(test_path)

    # Separate features and target
    X_train, y_train = train_data.drop(columns=['Target']), train_data['Target']
    X_validate, y_validate = validate_data.drop(columns=['Target']), validate_data['Target']
    X_test, y_test = test_data.drop(columns=['Target']), test_data['Target']

    # Impute missing values
    imputer = SimpleImputer(strategy="mean")
    X_train = pd.DataFrame(imputer.fit_transform(X_train), columns=X_train.columns)
    X_validate = pd.DataFrame(imputer.transform(X_validate), columns=X_validate.columns)
    X_test = pd.DataFrame(imputer.transform(X_test), columns=X_test.columns)

    # Define the parameter grid for GridSearch
    param_grid = {
        'penalty': ['l1', 'l2', 'elasticnet', 'none'],
        'C': [0.01, 0.1, 1, 10, 100],  # Regularization strength
        'solver': ['liblinear', 'lbfgs', 'saga'],  # Solvers for Logistic Regression
        'max_iter': [100, 500, 1000]  # Maximum number of iterations
    }

    # Initialize Logistic Regression and GridSearchCV
    logistic_model = LogisticRegression(random_state=42)
    grid_search = GridSearchCV(
        estimator=logistic_model,
        param_grid=param_grid,
        cv=5,  # 5-fold cross-validation
        scoring='accuracy',
        verbose=2,
        n_jobs=-1
    )

    # Perform grid search
    print("Starting Grid Search for Logistic Regression...")
    grid_search.fit(X_train, y_train)

    # Best parameters and best score
    print("\nBest Parameters:", grid_search.best_params_)
    print("Best Cross-Validation Accuracy:", grid_search.best_score_)

    # Train the final model on the entire training set with the best parameters
    best_model = grid_search.best_estimator_

    # Validate on validation set
    print("\n=== Validation Set Results ===")
    y_validate_pred = best_model.predict(X_validate)
    print("Accuracy:", accuracy_score(y_validate, y_validate_pred))
    print("\nClassification Report:\n", classification_report(y_validate, y_validate_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_validate, y_validate_pred))

    # Test on test set
    print("\n=== Test Set Results ===")
    y_test_pred = best_model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_test_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_test_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_test_pred))

    # Save the final model
    model_path = os.path.join(model_dir, 'logistic_regression_model.joblib')
    joblib.dump(best_model, model_path)
    print(f"Logistic Regression model saved to {model_path}")

