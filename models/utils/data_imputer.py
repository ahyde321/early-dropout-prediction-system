import miceforest as mf
import pandas as pd
import numpy as np

def apply_mice_imputation(combined_df, impute_columns, num_imputations=1, iterations=5):
    """
    Applies MICE imputation to the combined dataset on specified columns.
    - Validates columns and missing data
    - Converts data to float for compatibility
    - Applies miceforest MICE kernel and returns updated dataframe
    """

    # ✅ Filter to only existing columns
    impute_columns = [col for col in impute_columns if col in combined_df.columns]

    if not impute_columns:
        print("⚠️ No valid columns provided for imputation.")
        return combined_df

    # ✅ Check for missing values in selected columns
    missing_summary = combined_df[impute_columns].isna().sum()
    total_missing = missing_summary.sum()

    print("\n🔍 Missing Values Before Imputation:")
    print(missing_summary)

    if total_missing == 0:
        print("ℹ️ No missing values found. Skipping MICE imputation.")
        return combined_df

    # ✅ Prepare data (replace pd.NA with np.nan and ensure float dtype)
    mice_input = combined_df[impute_columns].copy().replace({pd.NA: np.nan})

    try:
        mice_input = mice_input.astype(float)
    except Exception as e:
        raise ValueError(f"Error converting imputation columns to float: {e}")

    # ✅ Apply MICE using miceforest
    try:
        kernel = mf.ImputationKernel(
            data=mice_input,
            num_datasets=num_imputations,
            random_state=42
        )
        kernel.mice(iterations=iterations)
    except Exception as e:
        raise RuntimeError(f"MICE imputation failed: {e}")

    # ✅ Retrieve and apply imputed values
    imputed_values = kernel.complete_data(0)

    print("\n✅ Missing Values After Imputation:")
    print(imputed_values.isna().sum())

    # ✅ Update the original dataframe
    combined_df[impute_columns] = imputed_values

    return combined_df
