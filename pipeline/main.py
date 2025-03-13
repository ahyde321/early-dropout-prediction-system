import os
import pandas as pd
from data_loader import load_data
from data_imputer import apply_mice_imputation
from data_cleaner import clean_data, separate_enrolled_students
from feature_selector import remove_highly_correlated_features, select_best_features
from data_aligner import align_datasets_and_combine

# Get the absolute path of the project directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define file paths using absolute paths
file1 = os.path.join(BASE_DIR, "../data/raw/raw_dataset1.csv")
file2 = os.path.join(BASE_DIR, "../data/raw/raw_dataset2.csv")

# Step 1: Load Data
df1, df2 = load_data(file1, file2)
print(f"🔍 Loaded Data: Dataset 1 - {df1.shape}, Dataset 2 - {df2.shape}")

# Step 2: Clean Data (Remove duplicates and empty rows early)
df1 = clean_data(df1)
df2 = clean_data(df2)
print(f"🧹 After Cleaning: Dataset 1 - {df1.shape}, Dataset 2 - {df2.shape}")

# Step 3: Align datasets and combine them
required_columns = ["Admission grade", "Previous qualification (grade)"]
combined_df = align_datasets_and_combine(df1, df2, required_columns)

print(f"✅ Combined Dataset Shape: {combined_df.shape}")

# Step 4: Apply MICE Imputation on the Combined Dataset
impute_columns = ["Admission grade", "Previous qualification (grade)"]
imputed_combined_df = apply_mice_imputation(combined_df, impute_columns)

print(f"✅ Imputation Complete: Combined Dataset Shape - {imputed_combined_df.shape}")

# Show a sample of the imputed columns
print("\n🔍 Sample of Imputed Data:")
print(imputed_combined_df[["Admission grade", "Previous qualification (grade)"]].head(10))
print(imputed_combined_df[["Admission grade", "Previous qualification (grade)"]].tail(10))

# Step 5: Separate 'Enrolled' Students and Save Both Datasets
cleaned_combined_df = separate_enrolled_students(
    imputed_combined_df,
    enrolled_path="data/filtered/enrolled.csv",
    filtered_path="data/filtered/past.csv"
)

print(f"🚀 Final Training Dataset Shape: {cleaned_combined_df.shape}")

# Step 6: Remove Highly Correlated Features from the Combined Dataset
cleaned_combined_df = remove_highly_correlated_features(cleaned_combined_df)

# Step 7: Select the Best Features for Model Training
final_dataset = select_best_features(cleaned_combined_df)

print(f"✅ Final Dataset Shape After Feature Selection: {final_dataset.shape}")



# # Step 6: Feature Selection
# df1 = remove_highly_correlated_features(df1)
# df2 = remove_highly_correlated_features(df2)
# print(f"📉 After Feature Selection: Dataset 1 - {df1.shape}, Dataset 2 - {df2.shape}")

# # Step 7: Preprocess for ML
# df1, encoders, scaler = preprocess_data(df1)
# df2, _, _ = preprocess_data(df2)

# # Step 8: Train Model
# model, accuracy = train_model(df1)
# print(f"🚀 Model Accuracy: {accuracy:.2f}")
