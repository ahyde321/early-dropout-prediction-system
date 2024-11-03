import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os
import joblib

# Set the base directory as one level up from the current script
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("Base directory:", base_dir)  # Check if this is the root directory

# File paths
data_file_path = os.path.join(base_dir, 'data', 'preprocessed_student_dropout_data.csv')
model_file_path = os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib')

# Load the data
data = pd.read_csv(data_file_path)

# Split the data into features (X) and target (y)
X = data.drop('Target', axis=1)
y = data['Target']

# Define numerical columns
numerical_columns = ['Age at enrollment', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
                     'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',
                     'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)',
                     'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
                     'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)',
                     'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)']

# Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize scalers
min_max_scaler = MinMaxScaler()
scaler = StandardScaler()

# Apply MinMax scaling to 'Age at enrollment'
X_train[['Age at enrollment']] = min_max_scaler.fit_transform(X_train[['Age at enrollment']])
X_test[['Age at enrollment']] = min_max_scaler.transform(X_test[['Age at enrollment']])

# Apply Standard scaling to other numerical columns
X_train[numerical_columns] = scaler.fit_transform(X_train[numerical_columns])
X_test[numerical_columns] = scaler.transform(X_test[numerical_columns])

feature_names = X_train.columns
joblib.dump(feature_names, os.path.join(base_dir, 'models', 'feature_names.joblib'))

# Choose and train the model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Feature Importance (For interpretability in Random Forests)
feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature Importances:\n", feature_importances.head(10))

# Save the model and scalers
os.makedirs(os.path.join(base_dir, 'models'), exist_ok=True)
joblib.dump(model, os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib'))
joblib.dump(scaler, os.path.join(base_dir, 'models', 'scaler.joblib'))
joblib.dump(min_max_scaler, os.path.join(base_dir, 'models', 'min_max_scaler.joblib'))
joblib.dump(numerical_columns, os.path.join(base_dir, 'models', 'numerical_columns.joblib'))

print("Model and scalers saved successfully.")
