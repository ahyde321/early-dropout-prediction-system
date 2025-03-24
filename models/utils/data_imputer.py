import miceforest as mf
import pandas as pd
import numpy as np

def apply_mice_imputation(combined_df, impute_columns, num_imputations=1, iterations=5):
    """
    Applies MICE imputation to the combined dataset on specified columns.
    - Checks that impute_columns exist.
    - Converts columns to float (replacing pd.NA with np.nan).
    - Runs the MICE imputation and returns the updated dataframe.
    """
    # Verify imputation columns are present
    missing_cols = [col for col in impute_columns if col not in combined_df.columns]
    if missing_cols:
        raise ValueError(f"Columns missing for imputation: {missing_cols}")
    
    print("\n🔍 Missing Values Before Imputation:")
    print(combined_df[impute_columns].isna().sum())
    
    # Prepare data for imputation
    mice_input = combined_df[impute_columns].copy().replace({pd.NA: np.nan})
    
    # Convert to float to ensure compatibility
    try:
        mice_input = mice_input.astype(float)
    except Exception as e:
        raise ValueError(f"Error converting imputation columns to float: {e}")
    
    try:
        # Initialize and run the MICE model
        kernel = mf.ImputationKernel(
            data=mice_input,
            num_datasets=num_imputations,
            random_state=42
        )
        kernel.mice(iterations=iterations)
    except Exception as e:
        raise RuntimeError(f"MICE imputation failed: {e}")
    
    # Retrieve the imputed data
    imputed_values = kernel.complete_data(0)
    
    print("\n✅ Missing Values After Imputation:")
    print(imputed_values.isna().sum())
    
    # Update the original dataframe with imputed values
    combined_df[impute_columns] = imputed_values
    
    return combined_df
