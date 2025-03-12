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

    print(f"✅ Cleaned Data: {df.shape[0]} rows remaining after cleaning.")
    return df


def separate_enrolled_students(df, save_path="data/enrolled/enrolled.csv"):
    """
    Separates students labeled as 'Enrolled' from the dataset and saves them to a CSV file.
    Ensures the training dataset contains only 'Graduate' and 'Dropout' students.

    Parameters:
    df (pd.DataFrame): The dataset containing student records.
    save_path (str): Path where the 'Enrolled' students will be saved.

    Returns:
    pd.DataFrame: Dataset without 'Enrolled' students.
    """
    initial_rows = df.shape[0]

    # Separate enrolled students
    enrolled_df = df[df["Target"] == "Enrolled"]
    df_filtered = df[df["Target"].isin(["Graduate", "Dropout"])]

    # Save enrolled students to a CSV file
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    enrolled_df.to_csv(save_path, index=False)

    print(f"🚀 Saved {len(enrolled_df)} 'Enrolled' students to {save_path}.")
    print(f"✅ Training dataset now contains {df_filtered.shape[0]} records (Graduate/Dropout only).")

    return df_filtered
