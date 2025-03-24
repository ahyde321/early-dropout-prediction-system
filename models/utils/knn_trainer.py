import os
import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

def train_optimized_knn(model_path, X_path, y_path):
    """
    Train a KNN model with hyperparameter tuning and save it to disk using pickle.
    
    Parameters:
        model_path (str): Path to save the trained model (.pkl).
        X_path (str): Path to training feature CSV.
        y_path (str): Path to training label CSV.
    """
    # ✅ Load data
    X_train = pd.read_csv(X_path)
    y_train = pd.read_csv(y_path).iloc[:, 0]

    # ✅ Define the KNN model and parameter grid
    knn = KNeighborsClassifier()
    param_grid = {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    }

    # ✅ Grid search with 5-fold cross-validation
    grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)

    # ✅ Get the best model
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    print("✅ Best KNN Parameters:", best_params)

    # ✅ Ensure model directory exists
    model_dir = os.path.dirname(model_path)
    os.makedirs(model_dir, exist_ok=True)

    # ✅ Save the trained model using pickle (for consistency)
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"✅ KNN model saved at: {model_path}")

    return {"best_params": best_params}
