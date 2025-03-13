import os
import sys
import pandas as pd

# Define paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

from pipeline.train_randomforest import train_random_forest

# File paths
train_dataset_path = os.path.join(base_dir, 'data', 'processed', 'train_dataset.csv')
test_dataset_path = os.path.join(base_dir, 'data', 'processed', 'test_dataset.csv')
validate_dataset_path = os.path.join(base_dir, 'data', 'processed', 'validate_dataset.csv')  # Optional
model_dir = os.path.join(base_dir, 'models')  # Directory to save models and scalers

# Train the model
print("Starting the training process...")

train_random_forest(
    train_dataset_path=train_dataset_path,
    test_dataset_path=test_dataset_path,
    validate_dataset_path=validate_dataset_path,
    model_dir=model_dir
)
print("Training completed successfully.")
