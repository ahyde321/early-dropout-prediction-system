import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def preprocess_student_dropout_data(input_file, output_file, enrolled_output_file=None):
    """
    Preprocess student dropout data by scaling numerical features, encoding categorical features,
    and saving the preprocessed dataset. If the 'Target' column is missing, it processes all rows as a single dataset.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the preprocessed CSV file.
        enrolled_output_file (str, optional): Path to save the preprocessed CSV file for "Enrolled". Only used if 'Target' column exists.
    """
    data = pd.read_csv(input_file)

    categorical_columns = ['Marital status', 'Application mode', 'Application order', 'Course',
                           'Daytime/evening attendance', 'Previous qualification', 'Nationality',
                           'Mother\'s qualification', 'Father\'s qualification', 'Mother\'s occupation',
                           'Father\'s occupation', 'Displaced', 'Educational special needs', 'Debtor',
                           'Tuition fees up to date', 'Gender', 'Scholarship holder', 'International']

    # Define preprocessing function
    def preprocess(data, categorical_columns):
        # Scale numerical features
        numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
        # Exclude non-numerical columns from scaling
        exclude_columns = ['Age at enrollment']
        if 'Target' in data.columns:
            exclude_columns.append('Target')
        numerical_columns = numerical_columns.difference(categorical_columns + exclude_columns)

        # Apply MinMax scaling to 'Age at enrollment'
        if 'Age at enrollment' in data.columns:
            min_max_scaler = MinMaxScaler()
            data['Age at enrollment'] = min_max_scaler.fit_transform(data[['Age at enrollment']])

        # Standardize other numerical features
        scaler = StandardScaler()
        data[numerical_columns] = scaler.fit_transform(data[numerical_columns])


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
        return data

    # Handle datasets with and without 'Target' column
    if 'Target' in data.columns:
        # Separate "Enrolled" students
        enrolled_data = data[data['Target'] == 'Enrolled']
        other_data = data[data['Target'] != 'Enrolled']

        # Encode the Target column for "Dropout" and "Graduate"
        other_data['Target'] = other_data['Target'].map({'Dropout': 1, 'Graduate': 0})

        # Preprocess both subsets
        other_data = preprocess(other_data, categorical_columns)
        enrolled_data = preprocess(enrolled_data, categorical_columns)

        # Save the preprocessed data
        other_data.to_csv(output_file, index=False)
        enrolled_data.to_csv(enrolled_output_file, index=False)

        print(f"Preprocessed data saved to {output_file}")
        print(f"Preprocessed enrolled data saved to {enrolled_output_file}")
    else:
        # Process the entire dataset if 'Target' is not present
        preprocessed_data = preprocess(data, categorical_columns)
        preprocessed_data.to_csv(output_file, index=False)

        print(f"Preprocessed data saved to {output_file}")
