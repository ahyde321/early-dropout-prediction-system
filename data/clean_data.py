import pandas as pd
import os

# Define paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
input_file = os.path.join(base_dir, 'data', 'raw', 'raw_dataset2.csv')  # Update with actual file path
output_file = os.path.join(base_dir, 'data', 'raw', 'cleaned_dataset2.csv')

# Define columns to remove
columns_to_drop = ["Marital status", "Nationality", "Mother's qualification", "Father's qualification"]

# Load dataset
print(f"Loading dataset from {input_file}...")
data = pd.read_csv(input_file)

# Drop specified columns
print(f"Removing columns: {columns_to_drop}")
data_cleaned = data.drop(columns=columns_to_drop, errors='ignore')

# Save cleaned dataset
os.makedirs(os.path.dirname(output_file), exist_ok=True)
data_cleaned.to_csv(output_file, index=False)

print(f"Cleaned dataset saved to {output_file}")
print("Remaining columns:", data_cleaned.columns.tolist())
