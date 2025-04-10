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
    if "application_mode" in df.columns:
        df = df.drop(columns=["application_mode"])
    else:
        print("⚠️ 'Application mode' column not found. Skipping drop.")

    print(f"✅ Cleaned Data: {df.shape[0]} rows remaining after cleaning.")
    return df


from pathlib import Path
import pandas as pd

def separate_enrolled_students(combined_df, enrolled_path=None, filtered_path=None):
    """
    Separates students labeled as 'Enrolled' from the combined dataset.
    Optionally saves 'Enrolled' and 'Graduate' + 'Dropout' students to CSVs.

    Parameters:
        combined_df (pd.DataFrame): The dataset containing student records.
        enrolled_path (str, optional): Path to save 'Enrolled' students.
        filtered_path (str, optional): Path to save 'Graduate' and 'Dropout' students.

    Returns:
        pd.DataFrame: DataFrame of 'Enrolled' students only.

    Raises:
        ValueError: If the 'target' column is missing.
    """
    if "target" not in combined_df.columns:
        raise ValueError("The 'target' column is missing from the dataset.")

    enrolled_df = combined_df[combined_df["target"] == "Enrolled"]
    df_filtered = combined_df[combined_df["target"].isin(["Graduate", "Dropout"])]

    # Conditionally save if paths are provided
    if enrolled_path:
        enrolled_dir = Path(enrolled_path).parent
        enrolled_dir.mkdir(parents=True, exist_ok=True)
        try:
            enrolled_df.to_csv(enrolled_path, index=False)
            print(f"🚀 Saved {len(enrolled_df)} 'Enrolled' students to {enrolled_path}.")
        except Exception as e:
            raise IOError(f"Error saving 'Enrolled' students to {enrolled_path}: {e}")

    if filtered_path:
        filtered_dir = Path(filtered_path).parent
        filtered_dir.mkdir(parents=True, exist_ok=True)
        try:
            df_filtered.to_csv(filtered_path, index=False)
            print(f"✅ Saved {df_filtered.shape[0]} 'Graduate' & 'Dropout' students to {filtered_path}.")
        except Exception as e:
            raise IOError(f"Error saving filtered students to {filtered_path}: {e}")

    return enrolled_df
