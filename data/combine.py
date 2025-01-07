import os
import pandas as pd

base_dir = os.path.abspath(os.path.dirname(__file__))

file1_path = os.path.join(base_dir, 'processed', 'preprocessed1.csv')
file2_path = os.path.join(base_dir, 'processed', 'preprocessed2.csv')
train_output_path = os.path.join(base_dir, 'train_dataset.csv')
validate_output_path = os.path.join(base_dir, 'validate_dataset.csv')

if not os.path.exists(file1_path):
    raise FileNotFoundError(f"File not found: {file1_path}")
if not os.path.exists(file2_path):
    raise FileNotFoundError(f"File not found: {file2_path}")

dataset1 = pd.read_csv(file1_path)
dataset2 = pd.read_csv(file2_path)

combined_dataset = pd.concat([dataset1, dataset2], axis=0)

# Shuffle the combined dataset
combined_dataset = combined_dataset.sample(frac=1, random_state=42).reset_index(drop=True)

# Split the dataset into 90% training and 10% validation
train_size = int(0.9 * len(combined_dataset))
train_dataset = combined_dataset.iloc[:train_size]
validate_dataset = combined_dataset.iloc[train_size:]

train_dataset.to_csv(train_output_path, index=False)
print(f"Training dataset saved to {train_output_path}")

validate_dataset.to_csv(validate_output_path, index=False)
print(f"Validation dataset saved to {validate_output_path}")
