from pathlib import Path

def clean_data(df):
    """
    Cleans the dataset by removing duplicate rows and fully empty rows.
    Also, it attempts to drop the 'Application mode' column if it exists.
    
    Parameters:
        df (pd.DataFrame): The input dataset.
    
    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    if df is None or df.empty:
        raise ValueError("The provided DataFrame is empty or None.")

    # Remove duplicate rows
    df = df.drop_duplicates()
    
    # Drop rows that are entirely empty
    df = df.dropna(how="all")
    
    # Attempt to drop 'Application mode' if present, else log a warning.
    if "Application mode" in df.columns:
        df = df.drop(columns=["Application mode"])
    else:
        print("⚠️ 'Application mode' column not found. Skipping drop.")

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
    
    Raises:
        ValueError: If the 'Target' column is missing.
    """
    # Check for the 'Target' column
    if "Target" not in combined_df.columns:
        raise ValueError("The 'Target' column is missing from the dataset.")
    
    # Separate 'Enrolled' students and 'Graduate' + 'Dropout' students
    enrolled_df = combined_df[combined_df["Target"] == "Enrolled"]
    df_filtered = combined_df[combined_df["Target"].isin(["Graduate", "Dropout"])]

    # Ensure the output directories exist
    enrolled_dir = Path(enrolled_path).parent
    filtered_dir = Path(filtered_path).parent
    enrolled_dir.mkdir(parents=True, exist_ok=True)
    filtered_dir.mkdir(parents=True, exist_ok=True)

    # Save the enrolled students dataset with error handling
    try:
        enrolled_df.to_csv(enrolled_path, index=False)
        print(f"🚀 Saved {len(enrolled_df)} 'Enrolled' students to {enrolled_path}.")
    except Exception as e:
        raise IOError(f"Error saving 'Enrolled' students to {enrolled_path}: {e}")

    # Save the filtered (Graduate & Dropout) dataset with error handling
    try:
        df_filtered.to_csv(filtered_path, index=False)
        print(f"✅ Saved {df_filtered.shape[0]} 'Graduate' & 'Dropout' students to {filtered_path}.")
    except Exception as e:
        raise IOError(f"Error saving filtered students to {filtered_path}: {e}")

    return df_filtered
