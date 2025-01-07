import os
from train_dropout_predictor import train_dropout_model

# Define the base directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Run the training function
print("Starting the training process...")
train_dropout_model(base_dir)
print("Training completed successfully.")
