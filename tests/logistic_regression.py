import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

from pipeline.train_logistic_regression import train_logistic_regression

train_path = os.path.join(base_dir, 'data', 'processed', 'train_dataset.csv')
validate_path = os.path.join(base_dir, 'data', 'processed', 'validate_dataset.csv')
test_path = os.path.join(base_dir, 'data', 'processed', 'test_dataset.csv')
model_dir = os.path.join(base_dir, 'models', 'logistic_regression')

for file_path in [train_path, validate_path, test_path]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

if __name__ == "__main__":
    print("Starting Logistic Regression training...")
    train_logistic_regression(train_path, validate_path, test_path, model_dir)
    print("Logistic Regression training completed.")
