import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dataset_path = os.path.join(base_dir, 'data', 'processed', 'train_dataset.csv')

if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

print(f"Dataset found at: {dataset_path}")

data = pd.read_csv(dataset_path)
if 'Target' not in data.columns:
    raise ValueError("Dataset must contain a 'Target' column.")

# Split data into features (X) and target (y)
X = data.drop('Target', axis=1)
y = data['Target']

# Split into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

param_grid = {'n_estimators': [50, 100, 200, 300, 400, 500]}

rf = RandomForestClassifier(random_state=42)

# Perform grid search with 5-fold cross-validation
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    scoring='accuracy',
    verbose=2,
    n_jobs=-1
)

print("Starting Grid Search...")
grid_search.fit(X_train, y_train)

# Get the best parameters and the corresponding score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("\n=== Grid Search Results ===")
print(f"Best Parameters: {best_params}")
print(f"Best Cross-Validation Accuracy: {best_score:.4f}")