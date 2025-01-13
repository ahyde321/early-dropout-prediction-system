import os
import sys

# Define paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

from pipeline.train_dropout_predictor import train_dropout_model

dataset_path = os.path.join(base_dir, 'data', 'processed', 'train_dataset.csv')
model_dir = os.path.join(base_dir, 'models')  # Directory to save models and scalers

# Train the model
print("Starting the training process...")
train_dropout_model(dataset_path, model_dir)
print("Training completed successfully.")
