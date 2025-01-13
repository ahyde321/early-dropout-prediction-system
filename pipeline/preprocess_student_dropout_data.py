import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def preprocess_student_dropout_data(input_file, output_file, enrolled_output_file=None, feature_names=None):
    """
    Preprocess student dropout data by scaling numerical features, encoding categorical features,
    and saving the preprocessed dataset. Ensures alignment with the model's expected feature names.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the preprocessed CSV file.
        enrolled_output_file (str, optional): Path to save the preprocessed CSV file for "Enrolled".
        feature_names (list, optional): List of features expected by the trained model.
    """
    data = pd.read_csv(input_file)

    categorical_columns = [
        'Marital status', 'Application mode', 'Application order', 'Course',
        'Daytime/evening attendance', 'Previous qualification', 'Nationality',
        'Mother\'s qualification', 'Father\'s qualification', 'Mother\'s occupation',
        'Father\'s occupation', 'Displaced', 'Educational special needs', 'Debtor',
        'Tuition fees up to date', 'Gender', 'Scholarship holder', 'International'
    ]

    def preprocess(data, categorical_columns):
        # Initialize scalers
        min_max_scaler = MinMaxScaler()
        scaler = StandardScaler()

        # Scale numerical features
        numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
        exclude_columns = ['Age at enrollment']
        if 'Target' in data.columns:
            exclude_columns.append('Target')
        numerical_columns = numerical_columns.difference(categorical_columns + exclude_columns)

        # Apply MinMax scaling to 'Age at enrollment'
        if 'Age at enrollment' in data.columns:
            data['Age at enrollment'] = min_max_scaler.fit_transform(data[['Age at enrollment']].astype('float64'))

        # Standardize other numerical features
        if len(numerical_columns) > 0:
            data[numerical_columns] = scaler.fit_transform(data[numerical_columns].astype('float64'))

        # Frequency encoding and one-hot encoding
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
            if col in data.columns:
                freq_encoding = data[col].value_counts() / len(data)
                data[col] = data[col].map(freq_encoding).astype('float64')

        data = pd.get_dummies(data, columns=one_hot_encode_columns, drop_first=True)

        # Add missing features with default values
        if feature_names:
            for feature in feature_names:
                if feature not in data.columns:
                    data[feature] = 0

        # Reorder columns to match the model's feature names
        if feature_names:
            data = data.reindex(columns=feature_names, fill_value=0)

        return data

    if 'Target' in data.columns:
        enrolled_data = data[data['Target'] == 'Enrolled'].copy()
        other_data = data[data['Target'] != 'Enrolled'].copy()

        # Map 'Dropout' to 1 and 'Graduate' to 0 in the Target column
        other_data['Target'] = other_data['Target'].map({'Dropout': 1, 'Graduate': 0})

        other_data = preprocess(other_data, categorical_columns)
        enrolled_data = preprocess(enrolled_data, categorical_columns)

        # Save preprocessed data to files
        other_data.to_csv(output_file, index=False)
        enrolled_data.to_csv(enrolled_output_file, index=False)

        print(f"Preprocessed data saved to {output_file}")
        print(f"Preprocessed enrolled data saved to {enrolled_output_file}")
    else:
        preprocessed_data = preprocess(data, categorical_columns)
        preprocessed_data.to_csv(output_file, index=False)

        print(f"Preprocessed data saved to {output_file}")