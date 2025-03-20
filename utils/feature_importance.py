import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# Load the trained model
with open("models/random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)

# Get feature importance
feature_importance = pd.DataFrame({
    "Feature": X_train.columns,  # Make sure X_train is accessible
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("🔍 Feature Importance:\n", feature_importance)
