import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

def train_random_forest(X_train_path, y_train_path, model_path, optimize=False, search_type="random", cv=5, n_iter=20):
    """
    Trains a Random Forest model with default parameters or optimizes hyperparameters using RandomizedSearchCV/GridSearchCV.
    
    Improvements:
    ✅ Logs **feature importance** after training.
    
    Parameters:
        X_train_path (str): Path to training features CSV.
        y_train_path (str): Path to training labels CSV.
        model_path (str): Path to save the trained model.
        optimize (bool): If True, performs hyperparameter optimization.
        search_type (str): "random" for RandomizedSearchCV (default), "grid" for GridSearchCV.
        cv (int): Number of cross-validation folds (default: 5).
        n_iter (int): Number of iterations for RandomizedSearchCV (ignored for GridSearchCV).

    Returns:
        dict: Best parameters if optimized, or default model confirmation.
    """

    # ✅ Load training data
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).values.ravel()

    if optimize:
        # ✅ Define hyperparameter grid for RandomForestClassifier
        param_grid = {
            "n_estimators": [50, 100, 200, 300, 500],
            "max_depth": [None, 10, 20, 30, 50],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "max_features": ["sqrt", "log2", None],
            "bootstrap": [True, False]
        }

        # ✅ Initialize RandomForestClassifier with class balancing
        model = RandomForestClassifier(class_weight="balanced", random_state=42)

        # ✅ Choose search method
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

        # ✅ Fit the search model
        search.fit(X_train, y_train)

        # ✅ Get the best model from the search
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

    # ✅ Save the feature importance to a CSV file for analysis
    feature_importance.to_csv("models/feature_importance.csv", index=False)

    # ✅ Save the trained model
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"✅ Model trained and saved at: {model_path}")
    print(f"📊 Feature importance saved to: models/feature_importance.csv")

    return {"best_params": best_params, "feature_importance": feature_importance}
