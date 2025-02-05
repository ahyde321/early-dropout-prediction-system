import os
import pandas as pd

base_dir = os.path.abspath(os.path.dirname(__file__))

# Define file paths
enrolled_file1 = os.path.join(base_dir, 'test', 'raw_enrolled1.csv')
enrolled_file2 = os.path.join(base_dir, 'test', 'raw_enrolled2.csv')
output_file = os.path.join(base_dir, 'test', 'raw_enrolled_dataset.csv')

# Load the datasets
print("Loading enrolled datasets...")
enrolled_data1 = pd.read_csv(enrolled_file1)
enrolled_data2 = pd.read_csv(enrolled_file2)

# Concatenate the datasets
print("Concatenating datasets...")
concatenated_data = pd.concat([enrolled_data1, enrolled_data2], ignore_index=True)

# Ensure directory exists for the output file
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Save the concatenated dataset
concatenated_data.to_csv(output_file, index=False)

print(f"Concatenated dataset saved to: {output_file}")