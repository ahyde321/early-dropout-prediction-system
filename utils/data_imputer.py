import miceforest as mf
import pandas as pd
import numpy as np

def apply_mice_imputation(combined_df, impute_columns, num_imputations=1, iterations=5):
    """
    Applies MICE imputation to the combined dataset.

    Parameters:
        combined_df (pd.DataFrame): The combined dataset with aligned columns.
        impute_columns (list): List of columns to impute.
        num_imputations (int): Number of imputed datasets to generate.
        iterations (int): Number of MICE iterations.

    Returns:
        pd.DataFrame: The fully imputed dataset.
    """

    # Log missing values before imputation
    print("\n🔍 Missing Values Before Imputation:")
    print(combined_df[impute_columns].isna().sum())

    # Ensure only the imputation columns are processed by MICE
    mice_input = combined_df[impute_columns].copy()

    # Replace pandas.NA with np.nan for compatibility
    mice_input = mice_input.replace({pd.NA: np.nan}).astype(float)

    # Train MICE model on the dataset
    kernel = mf.ImputationKernel(
        data=mice_input,
        num_datasets=num_imputations,
        random_state=42
    )

    # Run MICE
    kernel.mice(iterations=iterations)

    # Get the imputed dataset
    imputed_values = kernel.complete_data(0)

    # Log missing values after imputation
    print("\n✅ Missing Values After Imputation:")
    print(imputed_values.isna().sum())

    # Merge imputed values back into the full dataset
    combined_df[impute_columns] = imputed_values

    return combined_df
