import os
import pandas as pd
from data_loader import load_data
from data_imputer import apply_mice_imputation
from data_cleaner import clean_data, separate_enrolled_students
from feature_selector import remove_highly_correlated_features, select_best_features
from data_aligner import align_datasets_and_combine, align_enrolled_pupils
from data_preprocessor import preprocess_data
from data_splitter import split_train_val_test

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
past_pupils_df = separate_enrolled_students(
    imputed_combined_df,
    enrolled_path="data/filtered/enrolled_pupils.csv",
    filtered_path="data/filtered/past_pupils.csv"
)

print(f"🚀 Final Training Dataset Shape: {past_pupils_df.shape}")

# Step 6: Remove Highly Correlated Features from the Combined Dataset
past_pupils_df = remove_highly_correlated_features(past_pupils_df)

refined_past_pupil_path = os.path.join(BASE_DIR, "../data/refined/refined_past_pupil_dataset.csv")
refined_enrolled_pupil_path= os.path.join(BASE_DIR, "../data/refined/refined_enrolled_pupil_dataset.csv")

# Step 7: Select the Best Features for Model Training and Save
final_dataset = select_best_features(past_pupils_df)
final_dataset.to_csv(refined_past_pupil_path, index=False)

print(f"✅ Final Dataset Shape After Feature Selection: {final_dataset.shape}")

# Step 8: Align enrolled_pupil dataset to the past_pupil dataset
aligned_enrolled_df = align_enrolled_pupils(
    enrolled_path="data/filtered/enrolled_pupils.csv",
    final_dataset=final_dataset,
    output_path="data/refined/aligned_enrolled_pupils.csv"
)

# Step 9: Split data into 
split_train_val_test(
    input_path="data/refined/refined_past_pupil_dataset.csv",
    output_dir="data/ready"
)

# Step 10: Preprocess Enrolled and Past Pupil datasets
model_dir = os.path.join(BASE_DIR, "../models")

preprocessed_past_pupils = preprocess_data(
    input_path=refined_past_pupil_path,
    output_path="data/preprocessed/preprocessed_past_pupils.csv",
    model_dir=model_dir
)

preprocessed_enrolled_pupils = preprocess_data(
    input_path="data/refined/aligned_enrolled_pupils.csv",
    output_path="data/preprocessed/preprocessed_enrolled_pupils.csv",
    model_dir=model_dir
)

# # Step 8: Train Model
# model, accuracy = train_model(df1)
# print(f"🚀 Model Accuracy: {accuracy:.2f}")
