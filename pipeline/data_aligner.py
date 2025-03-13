import pandas as pd

def align_datasets_and_combine(df1, df2, required_columns):
    """
    Aligns two datasets by ensuring they have the same columns, then combines them.

    Parameters:
        df1 (pd.DataFrame): First dataset (e.g., data with missing values)
        df2 (pd.DataFrame): Second dataset (e.g., reference dataset with more complete values)
        required_columns (list): List of required columns to ensure consistency

    Returns:
        pd.DataFrame: A combined dataset with aligned columns
    """

    # Ensure both dataframes have all required columns
    for col in required_columns:
        if col not in df1.columns:
            df1[col] = pd.NA  # Add missing columns with NaN
        if col not in df2.columns:
            df2[col] = pd.NA

    # Ensure column order is the same for both datasets
    df1 = df1[sorted(df1.columns)]
    df2 = df2[sorted(df2.columns)]

    # Add marker column to track original datasets
    df1["dataset_marker"] = "df1"
    df2["dataset_marker"] = "df2"

    # Combine the datasets
    combined_df = pd.concat([df1, df2], ignore_index=True)

    return combined_df
