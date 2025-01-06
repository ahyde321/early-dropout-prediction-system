import pandas as pd

# Load the datasets
data1 = pd.read_csv('finalProject/data/raw_dataset.csv', delimiter=';')
data2 = pd.read_csv('/data/raw_dataset2.csv')                

# Add missing columns to each dataset for unionization
missing_cols_data1 = set(data2.columns) - set(data1.columns)
missing_cols_data2 = set(data1.columns) - set(data2.columns)

for col in missing_cols_data1:
    data1[col] = None

for col in missing_cols_data2:
    data2[col] = None

# Align column order and merge datasets
data1 = data1[data2.columns]  # Reorder columns in data1 to match data2
combined_data = pd.concat([data1, data2], ignore_index=True)

# Handle missing values
# Numeric columns: Fill missing values with median
numeric_cols = combined_data.select_dtypes(include=['float64', 'int64']).columns
combined_data[numeric_cols] = combined_data[numeric_cols].fillna(combined_data[numeric_cols].median())

# Categorical columns: Fill missing values with "Unknown"
categorical_cols = combined_data.select_dtypes(include=['object']).columns
combined_data[categorical_cols] = combined_data[categorical_cols].fillna("Unknown")

# Save the preprocessed dataset
combined_data.to_csv('/data/combined_dataset.csv', index=False)
