import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# File paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '../data/raw_dataset.csv')
save_path = os.path.join(script_dir, '../data/preprocessed_student_dropout_data.csv')

# Load the dataset
data = pd.read_csv(data_path)

categorical_columns = ['Marital status', 'Application mode', 'Application order', 'Course',
                       'Daytime/evening attendance', 'Previous qualification', 'Nationality',
                       'Mother\'s qualification', 'Father\'s qualification', 'Mother\'s occupation',
                       'Father\'s occupation', 'Displaced', 'Educational special needs', 'Debtor',
                       'Tuition fees up to date', 'Gender', 'Scholarship holder', 'International']

# Step 1: Filter the Target column to include only "Dropout" and "Graduate" and encode it
data = data[data['Target'] != 'Enrolled']  # Exclude "Enrolled"
data['Target'] = data['Target'].map({'Dropout': 1, 'Graduate': 0})

# Step 2: Scale numerical features
# Identify numerical columns, excluding categorical columns
numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
numerical_columns = numerical_columns.difference(categorical_columns + ['Target', 'Age at enrollment'])

# Apply MinMax scaling to 'Age at enrollment'
min_max_scaler = MinMaxScaler()
data['Age at enrollment'] = min_max_scaler.fit_transform(data[['Age at enrollment']])

# Standardize other numerical features
scaler = StandardScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# Step 3: Apply frequency encoding for large categories and one-hot encoding for smaller categories
freq_encode_columns = []
one_hot_encode_columns = []

# Determine which columns to frequency encode and which to one-hot encode
for col in categorical_columns:
    unique_values = data[col].nunique()
    if unique_values > 15:
        freq_encode_columns.append(col)
    else:
        one_hot_encode_columns.append(col)

# Apply frequency encoding
for col in freq_encode_columns:
    freq_encoding = data[col].value_counts() / len(data)
    data[col] = data[col].map(freq_encoding)

# Apply one-hot encoding for remaining categorical columns
data = pd.get_dummies(data, columns=one_hot_encode_columns, drop_first=True)

# Display the final preprocessed data
print("Frequency Encoded Columns:", freq_encode_columns)
print("One-Hot Encoded Columns:", one_hot_encode_columns)
print(data.head())

# Save the preprocessed dataset
data.to_csv(save_path, index=False)
print(f"Preprocessed data saved to {save_path}")
