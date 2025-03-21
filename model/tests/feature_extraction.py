import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV

# Load model
model = joblib.load("models/dropout_predictor_model.joblib")

# Extract the base estimator correctly
if isinstance(model, CalibratedClassifierCV):
    base_model = model._get_estimator()  # Correct way to get the base estimator
    feature_importance = base_model.feature_importances_
else:
    feature_importance = model.feature_importances_

# Convert to DataFrame
feature_importance_df = pd.DataFrame({
    "Feature": model.feature_names_in_,
    "Importance": feature_importance
}).sort_values(by="Importance", ascending=False)

# Save feature importance to a CSV file
feature_importance_df.to_csv("feature_importance.csv", index=False)

print("✅ Feature importance saved to feature_importance.csv")
