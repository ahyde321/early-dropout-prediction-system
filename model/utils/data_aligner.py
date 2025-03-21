import pandas as pd
from pathlib import Path

def align_datasets_and_combine(df1, df2, required_columns):
    """
    Aligns two datasets by ensuring they have the same columns.
    - Adds any missing required columns.
    - Reindexes both datasets to the union of their columns.
    - Adds a dataset marker to each.
    - Concatenates them into a single DataFrame.
    """
    # Ensure required columns exist in both dataframes
    for col in required_columns:
        if col not in df1.columns:
            df1[col] = pd.NA
        if col not in df2.columns:
            df2[col] = pd.NA

    # Determine the union of all columns from both dataframes
    all_columns = sorted(set(df1.columns).union(set(df2.columns)))
    
    # Reindex to enforce the same columns across both dataframes
    df1 = df1.reindex(columns=all_columns)
    df2 = df2.reindex(columns=all_columns)
    
    # Add a dataset marker to track the origin (avoid duplicates)
    if "dataset_marker" in df1.columns:
        df1 = df1.drop(columns=["dataset_marker"])
    if "dataset_marker" in df2.columns:
        df2 = df2.drop(columns=["dataset_marker"])
    df1["dataset_marker"] = "df1"
    df2["dataset_marker"] = "df2"
    
    # Combine the datasets
    combined_df = pd.concat([df1, df2], ignore_index=True)
    
    return combined_df



def align_enrolled_pupils(enrolled_path, final_dataset, output_path):
    """
    Aligns the enrolled pupils dataset with the final training dataset.
    - Loads the enrolled dataset from a file.
    - Drops the 'Target' column if present.
    - Reindexes to include all features from the final_dataset (excluding 'Target').
    - Saves the aligned dataset.
    """
    # Ensure the enrolled file exists
    enrolled_path = Path(enrolled_path)
    if not enrolled_path.exists():
        raise FileNotFoundError(f"Enrolled file not found: {enrolled_path}")
    
    try:
        enrolled_df = pd.read_csv(enrolled_path)
    except Exception as e:
        raise RuntimeError(f"Error reading enrolled dataset at {enrolled_path}: {e}")

    # Drop 'Target' column if it exists
    if "Target" in enrolled_df.columns:
        enrolled_df = enrolled_df.drop(columns=["Target"])
        print("🚀 'Target' column dropped from enrolled pupils dataset.")

    # Define the target feature set (final dataset columns excluding 'Target')
    target_features = [col for col in final_dataset.columns if col != "Target"]
    
    # Reindex the enrolled dataframe to include missing columns as NA
    aligned_enrolled_df = enrolled_df.reindex(columns=target_features, fill_value=pd.NA)
    
    # Warn if any columns are missing (shouldn't occur since reindex fills with NA)
    missing_cols = set(target_features) - set(aligned_enrolled_df.columns)
    if missing_cols:
        print(f"⚠️ Warning: Some columns missing after alignment: {missing_cols}")

    # Save the aligned dataset
    try:
        aligned_enrolled_df.to_csv(output_path, index=False)
        print(f"✅ Enrolled Dataset Aligned and Saved: {output_path}")
    except Exception as e:
        raise IOError(f"Error saving aligned dataset to {output_path}: {e}")

    return aligned_enrolled_df


