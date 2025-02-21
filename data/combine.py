import os
import pandas as pd

# Define base directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Define input file paths
file1_path = os.path.join(base_dir, 'raw', 'raw_dataset1.csv')
file2_path = os.path.join(base_dir, 'raw', 'raw_dataset2.csv')

# Define output file path
combined_output_path = os.path.join(base_dir, 'raw', 'combined_raw_dataset.csv')

# Ensure both input files exist
if not os.path.exists(file1_path):
    raise FileNotFoundError(f"File not found: {file1_path}")
if not os.path.exists(file2_path):
    raise FileNotFoundError(f"File not found: {file2_path}")

# Load datasets
dataset1 = pd.read_csv(file1_path)
dataset2 = pd.read_csv(file2_path)

# Combine datasets
combined_dataset = pd.concat([dataset1, dataset2], axis=0, ignore_index=True)

# Randomize (shuffle) dataset
combined_dataset = combined_dataset.sample(frac=1, random_state=42).reset_index(drop=True)

# Save combined dataset
combined_dataset.to_csv(combined_output_path, index=False)
print(f"✅ Combined and randomized dataset saved to {combined_output_path}")
