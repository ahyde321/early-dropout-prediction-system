import pandas as pd
import matplotlib.pyplot as plt

# Load both datasets
original_data = pd.read_csv('../data/raw_dataset.csv')
preprocessed_data = pd.read_csv('../data/preprocessed_student_dropout_data.csv')

# 1. Compare Summary Statistics
print("Original Data Statistics:")
print(original_data.describe())
print("\nPreprocessed Data Statistics:")
print(preprocessed_data.describe())

# 2. Visualise Distributions for a few columns (Example with 'Age at enrollment')
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
original_data['Age at enrollment'].plot(kind='hist', ax=axes[0], title='Original Age at Enrollment')
preprocessed_data['Age at enrollment'].plot(kind='hist', ax=axes[1], title='Preprocessed Age at Enrollment')
plt.show()

# 3. Compare categorical features (Example: Target column)
print("Original Target Value Counts:")
print(original_data['Target'].value_counts())
print("\nPreprocessed Target Value Counts:")
print(preprocessed_data['Target'].value_counts())
