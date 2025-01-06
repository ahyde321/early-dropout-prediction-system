import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def preprocess_student_dropout_data(input_file, output_file):
    """
    Preprocess student dropout data by scaling numerical features, encoding categorical features, 
    and saving the preprocessed dataset.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the preprocessed CSV file.
    """
    # Load the dataset
    data = pd.read_csv(input_file)

    categorical_columns = ['Marital status', 'Application mode', 'Application order', 'Course',
                           'Daytime/evening attendance', 'Previous qualification', 'Nationality',
                           'Mother\'s qualification', 'Father\'s qualification', 'Mother\'s occupation',
                           'Father\'s occupation', 'Displaced', 'Educational special needs', 'Debtor',
                           'Tuition fees up to date', 'Gender', 'Scholarship holder', 'International']

    # Filter the Target column to include only "Dropout" and "Graduate" and encode it
    data = data[data['Target'] != 'Enrolled']  # Exclude "Enrolled"
    data['Target'] = data['Target'].map({'Dropout': 1, 'Graduate': 0})

    # Scale numerical features, Identify numerical columns, excluding categorical columns
    numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
    numerical_columns = numerical_columns.difference(categorical_columns + ['Target', 'Age at enrollment'])

    # Apply MinMax scaling to 'Age at enrollment'
    min_max_scaler = MinMaxScaler()
    data['Age at enrollment'] = min_max_scaler.fit_transform(data[['Age at enrollment']])

    # Standardise other numerical features
    scaler = StandardScaler()
    data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

    # Frequency encoding for large categories and one-hot encoding for smaller categories
    freq_encode_columns = []
    one_hot_encode_columns = []

    for col in categorical_columns:
        if col in data.columns:
            unique_values = data[col].nunique()
            if unique_values > 15:
                freq_encode_columns.append(col)
            else:
                one_hot_encode_columns.append(col)

    for col in freq_encode_columns:
        freq_encoding = data[col].value_counts() / len(data)
        data[col] = data[col].map(freq_encoding)

    data = pd.get_dummies(data, columns=one_hot_encode_columns, drop_first=True)

    print("Frequency Encoded Columns:", freq_encode_columns)
    print("One-Hot Encoded Columns:", one_hot_encode_columns)
    print(data.head())

    data.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}")