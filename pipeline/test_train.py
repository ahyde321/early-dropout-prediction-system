import os
from train_dropout_predictor import train_dropout_model

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

dataset_path = os.path.join(base_dir, 'data', 'train_dataset.csv')
model_dir = os.path.join(base_dir, 'models')  # Directory to save models and scalers

print("Starting the training process...")
train_dropout_model(dataset_path, model_dir)
print("Training completed successfully.")
