import os
from train_dropout_predictor import train_dropout_model

# Define the base directory (root directory of the project)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Moves up one directory level

# Define paths
dataset_path = os.path.join(base_dir, 'data', 'train_dataset.csv')  # Correct path to 'data/train_dataset.csv'
model_dir = os.path.join(base_dir, 'models')  # Directory to save models and scalers

# Run the training function
print("Starting the training process...")
train_dropout_model(dataset_path, model_dir)
print("Training completed successfully.")
