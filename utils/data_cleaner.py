import pandas as pd
import os

def clean_data(df):
    """
    Cleans the dataset by removing duplicate rows and fully empty rows.
    Preserves missing values for imputation.

    Parameters:
    df (pd.DataFrame): The input dataset.

    Returns:
    pd.DataFrame: Cleaned dataset.
    """
    df = df.drop_duplicates()  # Remove duplicate rows
    df = df.dropna(how="all")  # Drop only fully empty rows
    df = df.drop(columns=["Application Mode"])

    print(f"✅ Cleaned Data: {df.shape[0]} rows remaining after cleaning.")
    return df

def separate_enrolled_students(combined_df, enrolled_path="data/filtered/enrolled.csv", filtered_path="data/filtered/past.csv"):
    """
    Separates students labeled as 'Enrolled' from the combined dataset and saves them separately.
    Saves 'Enrolled' students in one file and 'Graduate' + 'Dropout' students in another.

    Parameters:
    combined_df (pd.DataFrame): The dataset containing student records.
    enrolled_path (str): Path to save 'Enrolled' students.
    filtered_path (str): Path to save 'Graduate' and 'Dropout' students.

    Returns:
    pd.DataFrame: Dataset with only 'Graduate' and 'Dropout' students.
    """
    initial_rows = combined_df.shape[0]

    # Separate 'Enrolled' students
    enrolled_df = combined_df[combined_df["Target"] == "Enrolled"]
    df_filtered = combined_df[combined_df["Target"].isin(["Graduate", "Dropout"])]

    # Ensure directories exist before saving
    os.makedirs(os.path.dirname(enrolled_path), exist_ok=True)
    os.makedirs(os.path.dirname(filtered_path), exist_ok=True)

    # Save 'Enrolled' students
    enrolled_df.to_csv(enrolled_path, index=False)
    print(f"🚀 Saved {len(enrolled_df)} 'Enrolled' students to {enrolled_path}.")

    # Save 'Graduate' and 'Dropout' students
    df_filtered.to_csv(filtered_path, index=False)
    print(f"✅ Saved {df_filtered.shape[0]} 'Graduate' & 'Dropout' students to {filtered_path}.")

    return df_filtered
