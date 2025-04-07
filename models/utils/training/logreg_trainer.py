import os
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

def train_logistic_regression(X_train_path, y_train_path, model_path):
    """
    Train a Logistic Regression model with hyperparameter optimization and save it using pickle.

    Parameters:
        X_train_path (str): Path to the training feature CSV.
        y_train_path (str): Path to the training label CSV.
        model_path (str): Path to save the trained model.
    """
    # Load data
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).iloc[:, 0]

    # Define Logistic Regression and parameter grid
    logreg = LogisticRegression(solver="liblinear", class_weight="balanced")
    param_grid = {
        'C': [0.01, 0.1, 1, 10, 100],
        'penalty': ['l1', 'l2']
    }

    # Grid search with 5-fold CV
    grid_search = GridSearchCV(logreg, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    print("✅ Best Logistic Regression Parameters:", best_params)

    # Ensure model directory exists
    model_dir = os.path.dirname(model_path)
    os.makedirs(model_dir, exist_ok=True)

    # Save the model using pickle
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"✅ Logistic Regression model saved at: {model_path}")

    return {"best_params": best_params}
