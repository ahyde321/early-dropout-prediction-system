import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Load the dataset
data = pd.read_csv('../data/raw_dataset.csv')

# Step 1: Filter the Target column to include only "Dropout" and "Graduate" and encode it
data = data[data['Target'] != 'Enrolled']  # Exclude "Enrolled"
data['Target'] = data['Target'].map({'Dropout': 1, 'Graduate': 0})

# Step 2: Scale numerical features
# Separate out 'Age at enrollment' to use MinMaxScaler, and standardise others
numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns.drop(['Target', 'Age at enrollment'])

# Apply MinMax scaling to 'Age at enrollment'
min_max_scaler = MinMaxScaler()
data['Age at enrollment'] = min_max_scaler.fit_transform(data[['Age at enrollment']])

# Standardize other numerical features
scaler = StandardScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# Step 3: One-hot encode categorical columns
categorical_columns = ['Marital status', 'Application mode', 'Application order', 'Course',
                       'Daytime/evening attendance', 'Previous qualification', 'Nacionality',
                       'Mother\'s qualification', 'Father\'s qualification', 'Mother\'s occupation',
                       'Father\'s occupation', 'Displaced', 'Educational special needs', 'Debtor',
                       'Tuition fees up to date', 'Gender', 'Scholarship holder', 'International']

# One-hot encode categorical columns, dropping the first category 
data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)

# Display the final preprocessed data
print(data.head())

# Save the preprocessed dataset
data.to_csv('../data/preprocessed_student_dropout_data.csv', index=False)

