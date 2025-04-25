import pandas as pd
import pickle
import os
import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, StratifiedKFold
from sklearn.metrics import precision_recall_curve


# Allow access to utils even when run directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def train_random_forest(
    X_train_path,
    y_train_path,
    model_path,
    optimize=False,
    search_type="random",
    cv=5,
    n_iter=20,
    early_stop_cv_score_threshold=None,
    param_grid_override=None
):
    """
    Trains a Random Forest model with default parameters or optimizes hyperparameters using RandomizedSearchCV/GridSearchCV.
    Adds strong regularization defaults to prevent overfitting.

    Parameters:
        X_train_path (str): Path to training features CSV.
        y_train_path (str): Path to training labels CSV.
        model_path (str): Path to save the trained model.
        optimize (bool): If True, performs hyperparameter optimization.
        search_type (str): "random" or "grid"
        cv (int): Cross-validation folds.
        n_iter (int): Iterations for RandomizedSearchCV (ignored for GridSearchCV).
        early_stop_cv_score_threshold (float): Optional early stopping if mean CV score < threshold.
        param_grid_override (dict): Optional custom hyperparameter grid to override the default.

    Returns:
        dict: Best parameters and feature importance DataFrame.
    """

    # ✅ Load training data
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).values.ravel()

    # ✅ Hyperparameter optimization or default model
    if optimize:
        param_grid = param_grid_override if param_grid_override is not None else {
            "n_estimators": [50, 100, 200, 300, 500],
            "max_depth": [6, 8, 10, 12, None],
            "min_samples_split": [5, 10, 20],
            "min_samples_leaf": [2, 4, 6],
            "max_features": ["sqrt", "log2"],
            "bootstrap": [True],
            "class_weight": ["balanced"]
        }

        model = RandomForestClassifier(random_state=42)

        if search_type == "random":
            print("🔍 Running Randomized Search for Random Forest...")
            search = RandomizedSearchCV(
                estimator=model,
                param_distributions=param_grid,
                n_iter=n_iter,
                cv=StratifiedKFold(n_splits=cv, shuffle=True, random_state=42),
                verbose=2,
                n_jobs=-1,
                random_state=42
            )
        elif search_type == "grid":
            print("🔍 Running Grid Search for Random Forest...")
            search = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=StratifiedKFold(n_splits=cv, shuffle=True, random_state=42),
                verbose=2,
                n_jobs=-1
            )
        else:
            raise ValueError("Invalid search_type. Use 'random' or 'grid'.")

        search.fit(X_train, y_train)
        best_model = search.best_estimator_
        best_params = search.best_params_
        mean_cv_score = search.best_score_

        print("\n✅ Best Random Forest Hyperparameters:", best_params)
        print(f"📈 Best CV Score: {mean_cv_score:.4f}")

        if early_stop_cv_score_threshold and mean_cv_score < early_stop_cv_score_threshold:
            print(f"⛔ Early stopping: best CV score {mean_cv_score:.4f} < threshold {early_stop_cv_score_threshold}")
            return {"best_params": best_params, "feature_importance": None}

    else:
        print("🚀 Training Random Forest with default anti-overfit parameters...")
        best_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_split=10,
            min_samples_leaf=4,
            max_features="sqrt",
            bootstrap=True,
            class_weight="balanced",
            random_state=42
        )
        best_model.fit(X_train, y_train)
        best_params = "Default (regularized) parameters used."

    # ✅ Threshold tuning (F1 optimization)
    if hasattr(best_model, "predict_proba"):
        print("\n🎯 Tuning threshold for best F1 score...")
        probs = best_model.predict_proba(X_train)[:, 1]
        precision, recall, thresholds = precision_recall_curve(y_train, probs)
        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-6)
        best_threshold = thresholds[np.argmax(f1_scores)]
        print(f"✅ Best threshold for F1: {best_threshold:.3f}")
    else:
        best_threshold = 0.5
        print("⚠️ Model does not support predict_proba. Using default threshold = 0.5")

    # ✅ Log Feature Importance
    assert isinstance(best_model, RandomForestClassifier)
    feature_importance = pd.DataFrame({
        "Feature": X_train.columns,
        "Importance": best_model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    print("\n🔍 Feature Importance:")
    print(feature_importance)

    # ✅ Save model and feature importance
    model_dir = os.path.dirname(model_path)
    os.makedirs(model_dir, exist_ok=True)

    feature_path = os.path.join(model_dir, "feature_importance.csv")
    feature_importance.to_csv(feature_path, index=False)

    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"✅ Model saved at: {model_path}")
    print(f"📊 Feature importance saved at: {feature_path}")

    return {
        "best_params": best_params,
        "feature_importance": feature_importance,
        "threshold": best_threshold
    }