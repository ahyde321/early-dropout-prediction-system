import pandas as pd
import miceforest as mf

def align_and_impute_datasets(df1, df2, impute_columns, iterations=5):
    """
    Ensures both datasets have the same structure by aligning columns and 
    applying MICE imputation to missing numeric values.

    Parameters:
    df1 (pd.DataFrame): First dataset.
    df2 (pd.DataFrame): Second dataset.
    impute_columns (list): List of numeric columns to apply MICE on.
    iterations (int): Number of MICE iterations.

    Returns:
    tuple: Aligned and imputed df1, df2.
    """
    all_columns = set(df1.columns).union(set(df2.columns))

    # Add missing columns to each dataset (fill with NaN so MICE can handle it)
    for col in all_columns:
        if col not in df1.columns:
            df1[col] = None  # Preserve NaNs for imputation
        if col not in df2.columns:
            df2[col] = None

    # Reorder both datasets to match column order
    df1 = df1[list(all_columns)]
    df2 = df2[list(all_columns)]

    # Apply MICE only to selected numeric columns
    available_impute_columns = [col for col in impute_columns if col in df1.columns]

    if available_impute_columns:
        print(f"🔍 Applying MICE to: {available_impute_columns}")

        for df in [df1, df2]:
            kernel = mf.ImputationKernel(df[available_impute_columns], datasets=5, save_all_iterations=True, random_state=42)
            kernel.mice(iterations)
            df[available_impute_columns] = kernel.complete_data()

        print("✅ MICE Imputation Completed.")

    return df1, df2
