import os
import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.compose import ColumnTransformer


def train_optimized_knn(model_path, X_path, y_path):
    """
    Train a KNN model with preprocessing, feature selection, and hyperparameter tuning, then save it to disk.

    Parameters:
        model_path (str): Path to save the trained model (.pkl).
        X_path (str): Path to training feature CSV.
        y_path (str): Path to training label CSV.
    """
    # ✅ Load data
    X_train = pd.read_csv(X_path)
    y_train = pd.read_csv(y_path).iloc[:, 0]

    # ✅ Preprocessing pipeline: scaling + feature selection + KNN
    preprocessor = Pipeline([
        ('scaler', StandardScaler()),
        ('select', SelectKBest(score_func=f_classif, k='all'))  # Optional: Set k to a number to filter
    ])

    pipe = Pipeline([
        ('pre', preprocessor),
        ('knn', KNeighborsClassifier())
    ])

    # ✅ Define hyperparameter grid
    param_grid = {
        'knn__n_neighbors': [5, 7, 9, 11, 13],
        'knn__weights': ['uniform', 'distance'],
        'knn__p': [1, 2],  # Manhattan vs Euclidean
        'knn__leaf_size': [10, 20, 40]
    }

    # ✅ Grid search with 5-fold cross-validation
    grid_search = GridSearchCV(pipe, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)

    # ✅ Best model
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    print("✅ Best KNN Parameters:", best_params)

    # ✅ Ensure model directory exists
    model_dir = os.path.dirname(model_path)
    os.makedirs(model_dir, exist_ok=True)

    # ✅ Save the model
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"✅ KNN model saved at: {model_path}")
    return {"best_params": best_params}