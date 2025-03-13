import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer

# Define columns to remove
columns_to_remove = ["Marital status", "Nationality", "Mother's qualification", "Father's qualification"]

def preprocess_student_dropout_data(input_file, output_dir, enrolled_output_file=None, raw_enrolled_output_file=None, feature_names=None):
    """
    Preprocess student dropout data by removing unnecessary columns, handling missing values, scaling numerical features, encoding categorical features,
    and splitting into training, validation, and test datasets with stratified sampling and controlled oversampling.

    Args:
        input_file (str): Path to the input CSV file.
        output_dir (str): Directory to save processed datasets.
        enrolled_output_file (str, optional): Path to save the preprocessed dataset for "Enrolled" students.
        raw_enrolled_output_file (str, optional): Path to save the raw dataset for "Enrolled" students.
        feature_names (list, optional): List of features expected by the trained model.
    """
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    # Load dataset
    data = pd.read_csv(input_file)

    # Remove specified columns
    print(f"Removing columns: {columns_to_remove}")
    data = data.drop(columns=columns_to_remove, errors='ignore')

    categorical_columns = [
        'Application mode', 'Application order', 'Course',
        'Daytime/evening attendance', 'Previous qualification',
        "Mother's occupation", "Father's occupation", 'Displaced',
        'Educational special needs', 'Debtor', 'Tuition fees up to date',
        'Gender', 'Scholarship holder', 'International'
    ]

    def preprocess(data, categorical_columns):
        min_max_scaler = MinMaxScaler()
        scaler = StandardScaler()

        numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
        exclude_columns = ['Age at enrollment']
        if 'Target' in data.columns:
            exclude_columns.append('Target')
        numerical_columns = numerical_columns.difference(categorical_columns + exclude_columns)

        # Handle missing values by imputing with median
        imputer = SimpleImputer(strategy="median")
        data[numerical_columns] = imputer.fit_transform(data[numerical_columns])

        # Scale "Age at enrollment"
        if 'Age at enrollment' in data.columns:
            data['Age at enrollment'] = min_max_scaler.fit_transform(data[['Age at enrollment']].astype('float64'))

        # Scale other numerical features
        if len(numerical_columns) > 0:
            data[numerical_columns] = scaler.fit_transform(data[numerical_columns].astype('float64'))

        freq_encode_columns = []
        one_hot_encode_columns = []

        # Decide which encoding to apply
        for col in categorical_columns:
            if col in data.columns:
                unique_values = data[col].nunique()
                if unique_values > 15:
                    freq_encode_columns.append(col)
                else:
                    one_hot_encode_columns.append(col)

        # Apply Frequency Encoding
        for col in freq_encode_columns:
            if col in data.columns:
                freq_encoding = data[col].value_counts() / len(data)
                data[col] = data[col].map(freq_encoding).astype('float64')

        # Apply One-Hot Encoding
        data = pd.get_dummies(data, columns=one_hot_encode_columns, drop_first=True)

        # Ensure feature alignment
        if feature_names:
            for feature in feature_names:
                if feature not in data.columns:
                    data[feature] = 0  # Add missing features with default value 0

            data = data.reindex(columns=feature_names, fill_value=0)

        return data

    # Handle Enrolled Students Separately
    if 'Target' in data.columns:
        enrolled_data = data[data['Target'] == 'Enrolled'].copy()
        other_data = data[data['Target'] != 'Enrolled'].copy()

        # Save raw enrolled data
        if raw_enrolled_output_file:
            enrolled_data.to_csv(raw_enrolled_output_file, index=False)
            print(f"Raw enrolled data saved to {raw_enrolled_output_file}")

        # Convert Target labels for training data (Dropout → 1, Graduate → 0)
        other_data['Target'] = other_data['Target'].map({'Dropout': 1, 'Graduate': 0})

        # Preprocess datasets
        other_data = preprocess(other_data, categorical_columns)
        enrolled_data = preprocess(enrolled_data, categorical_columns)

        # Split Data into Train, Validate, and Test with Stratified Sampling
        train_data, temp_data = train_test_split(other_data, test_size=0.3, random_state=42, stratify=other_data['Target'])
        validate_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42, stratify=temp_data['Target'])

        # Apply SMOTE with controlled oversampling
        dropout_count = sum(train_data['Target'] == 1)
        graduate_count = sum(train_data['Target'] == 0)
        desired_dropout_count = int(graduate_count * 0.9)  # Dropouts should be at most 90% of graduates

        if dropout_count < desired_dropout_count:
            sampling_strategy = min(1.0, desired_dropout_count / dropout_count)  # Ensure max value is 1.0
        else:
            sampling_strategy = 1.0  # No oversampling needed

        smote = SMOTE(sampling_strategy=sampling_strategy, random_state=42)
        X_train, y_train = train_data.drop(columns=['Target']), train_data['Target']
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

        # Recombine after oversampling
        train_data = pd.concat([pd.DataFrame(X_train_resampled, columns=X_train.columns),
                                pd.Series(y_train_resampled, name='Target')], axis=1)

        # Save Train, Validate, and Test datasets
        train_file = os.path.join(output_dir, "train_dataset.csv")
        validate_file = os.path.join(output_dir, "validate_dataset.csv")
        test_file = os.path.join(output_dir, "test_dataset.csv")

        train_data.to_csv(train_file, index=False)
        validate_data.to_csv(validate_file, index=False)
        test_data.to_csv(test_file, index=False)

        print(f"✅ Training dataset saved to {train_file}")
        print(f"✅ Validation dataset saved to {validate_file}")
        print(f"✅ Test dataset saved to {test_file}")

        # Save Preprocessed Enrolled Data
        if enrolled_output_file:
            enrolled_data.to_csv(enrolled_output_file, index=False)
            print(f"✅ Preprocessed enrolled data saved to {enrolled_output_file}")
