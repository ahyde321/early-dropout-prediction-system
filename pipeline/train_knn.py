import os
import sys
import pandas as pd
from sklearn.impute import SimpleImputer

# Add the project root directory to sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

from pipeline.train_knn import train_knn_with_kfold

# Define file paths
train_path = os.path.join(base_dir, 'data', 'processed', 'train_dataset.csv')
validate_path = os.path.join(base_dir, 'data', 'processed', 'validate_dataset.csv')
test_path = os.path.join(base_dir, 'data', 'processed', 'test_dataset.csv')
model_dir = os.path.join(base_dir, 'models', 'knn')

# Load datasets
train_data = pd.read_csv(train_path)
validate_data = pd.read_csv(validate_path)
test_data = pd.read_csv(test_path)

# Impute missing values and handle data type issues
imputer = SimpleImputer(strategy="mean")

def impute_and_cast(data):
    imputed_data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)
    for col in data.columns:
        if data[col].dtype == 'bool':
            imputed_data[col] = imputed_data[col].astype(bool)  # Cast back to boolean
        elif data[col].dtype == 'int64':
            imputed_data[col] = imputed_data[col].astype(int)  # Cast back to integer
    return imputed_data

train_data = impute_and_cast(train_data)
validate_data = impute_and_cast(validate_data)
test_data = impute_and_cast(test_data)

# Save the imputed datasets (optional, for debugging purposes)
imputed_train_path = os.path.join(base_dir, 'data', 'processed', 'train_dataset_imputed.csv')
imputed_validate_path = os.path.join(base_dir, 'data', 'processed', 'validate_dataset_imputed.csv')
imputed_test_path = os.path.join(base_dir, 'data', 'processed', 'test_dataset_imputed.csv')

train_data.to_csv(imputed_train_path, index=False)
validate_data.to_csv(imputed_validate_path, index=False)
test_data.to_csv(imputed_test_path, index=False)

print(f"Imputed train dataset saved to: {imputed_train_path}")
print(f"Imputed validate dataset saved to: {imputed_validate_path}")
print(f"Imputed test dataset saved to: {imputed_test_path}")

# Run KNN training with K-Fold Cross-Validation
if __name__ == "__main__":
    print("Starting KNN training with K-Fold Cross-Validation...")
    
    # Modify train_knn_with_kfold to return optimal parameters
    optimal_params = train_knn_with_kfold(
        imputed_train_path, 
        imputed_validate_path, 
        imputed_test_path, 
        model_dir
    )
    
    print("KNN training and evaluation completed.")
    print(f"Optimal parameters: {optimal_params}")
