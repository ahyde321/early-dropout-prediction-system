import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

def train_random_forest(X_train_path, y_train_path, model_path, optimize=False, search_type="random", cv=5, n_iter=20):
    """
    Trains a Random Forest model with default parameters or optimizes hyperparameters using RandomizedSearchCV/GridSearchCV.

    Parameters:
        X_train_path (str): Path to training features CSV.
        y_train_path (str): Path to training labels CSV.
        model_path (str): Path to save the trained model.
        optimize (bool): If True, performs hyperparameter optimization.
        search_type (str): "random" or "grid"
        cv (int): Cross-validation folds.
        n_iter (int): Iterations for RandomizedSearchCV (ignored for GridSearchCV).

    Returns:
        dict: Best parameters and feature importance DataFrame.
    """

    # ✅ Load training data
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).values.ravel()

    # ✅ Hyperparameter optimization or default model
    if optimize:
        param_grid = {
            "n_estimators": [50, 100, 200, 300, 500],
            "max_depth": [None, 10, 20, 30, 50],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "max_features": ["sqrt", "log2", None],
            "bootstrap": [True, False]
        }

        model = RandomForestClassifier(class_weight="balanced", random_state=42)

        if search_type == "random":
            print("🔍 Running Randomized Search for Random Forest...")
            search = RandomizedSearchCV(
                estimator=model,
                param_distributions=param_grid,
                n_iter=n_iter,
                cv=cv,
                verbose=2,
                n_jobs=-1,
                random_state=42
            )
        elif search_type == "grid":
            print("🔍 Running Grid Search for Random Forest...")
            search = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=cv,
                verbose=2,
                n_jobs=-1
            )
        else:
            raise ValueError("Invalid search_type. Use 'random' or 'grid'.")

        search.fit(X_train, y_train)
        best_model = search.best_estimator_
        best_params = search.best_params_
        print("\n✅ Best Random Forest Hyperparameters:", best_params)

    else:
        print("🚀 Training Random Forest with default parameters...")
        best_model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
        best_model.fit(X_train, y_train)
        best_params = "Default parameters used."

    # ✅ Log Feature Importance
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

    return {"best_params": best_params, "feature_importance": feature_importance}
