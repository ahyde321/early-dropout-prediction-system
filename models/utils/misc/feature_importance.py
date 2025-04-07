from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os

# Load dataset
input_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/raw/combined_raw_dataset.csv"))
df = pd.read_csv(input_file)

# Drop "Enrolled" students
df = df[df["Target"].isin(["Graduate", "Dropout"])]

# Encode target labels (Graduate = 0, Dropout = 1)
label_encoder = LabelEncoder()
df["Target"] = label_encoder.fit_transform(df["Target"])  # Convert categorical target to numeric

# Prepare dataset
X = df.drop(columns=["Target"])
y = df["Target"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Get feature importance
importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("Feature Importance:")
print(importance)

# Compute correlation with dropout target
correlation = df.corr()["Target"].sort_values(ascending=False)  # Now target is numeric
print("\nCorrelation with Dropout Target:")
print(correlation)
