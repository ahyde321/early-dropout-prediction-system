import os
import pandas as pd
import pickle
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold

def train_xgboost(X_train_path, y_train_path, model_path):
    """
    Train an XGBoost model with hyperparameter tuning and save it using pickle.

    Parameters:
        X_train_path (str): Path to the training feature CSV.
        y_train_path (str): Path to the training label CSV.
        model_path (str): Path to save the trained model.
    """
    # Load training data
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).iloc[:, 0]

    # Define model and parameter grid
    xgb = XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        n_jobs=-1,
        random_state=42
    )

    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    grid_search = GridSearchCV(
        estimator=xgb,
        param_grid=param_grid,
        cv=cv,
        scoring='f1',
        verbose=1,
        n_jobs=-1
    )

    # Fit and get best model
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    print("✅ Best XGBoost Parameters:", best_params)

    # Ensure model directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save best model
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"✅ XGBoost model saved at: {model_path}")
    return {"best_params": best_params}
