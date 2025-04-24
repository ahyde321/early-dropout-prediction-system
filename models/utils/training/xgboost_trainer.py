import os
import pandas as pd
import pickle
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def train_xgboost(X_train_path, y_train_path, model_path):
    """
    Train an XGBoost model with hyperparameter tuning, scaling, and save it using pickle.

    Parameters:
        X_train_path (str): Path to the training feature CSV.
        y_train_path (str): Path to the training label CSV.
        model_path (str): Path to save the trained model.
    """
    # Load training data
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).iloc[:, 0]

    # Define preprocessing pipeline (scaling + XGBoost)
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('xgb', XGBClassifier(
            objective='binary:logistic',
            eval_metric='logloss',
            n_jobs=-1,
            random_state=42
        ))
    ])

    # Define hyperparameter grid
    param_grid = {
        'xgb__n_estimators': [100, 200, 300],
        'xgb__max_depth': [3, 5, 7],
        'xgb__learning_rate': [0.01, 0.1, 0.2],
        'xgb__subsample': [0.8, 1.0],
        'xgb__colsample_bytree': [0.8, 1.0],
        'xgb__gamma': [0, 0.1, 0.2]  # Regularization parameter
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=cv,
        scoring='f1',
        verbose=1,
        n_jobs=-1
    )

    # Fit the grid search
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