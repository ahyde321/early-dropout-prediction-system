import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_val_test(input_path, output_dir, test_size=0.15, val_size=0.15, random_state=42):
    """
    Splits the dataset into training, validation, and test sets.

    Enhancements:
    - Checks for the existence and readability of the input file.
    - Verifies that the DataFrame is not empty.
    - Confirms the 'target' column is present.
    - Wraps the split and file saving operations in try/except blocks.
    - Logs dataset shapes at each step.

    Parameters:
        input_path (str): Path to the dataset CSV file.
        output_dir (str): Directory to save the split datasets.
        test_size (float): Proportion of data for the test set.
        val_size (float): Proportion of data for the validation set.
        random_state (int): Random seed for reproducibility.

    Returns:
        None (saves split datasets as CSV files in output_dir)
    """
    # Check that input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Load dataset
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        raise RuntimeError(f"Error reading the input CSV file: {e}")

    # Check if DataFrame is empty
    if df.empty:
        raise ValueError(f"The input file {input_path} is empty.")

    # Verify that the target column exists
    if "target" not in df.columns:
        raise ValueError("The 'target' column is missing from the dataset.")

    # Separate features and target
    try:
        X = df.drop(columns=["target"])
        y = df["target"]
    except Exception as e:
        raise RuntimeError(f"Error separating features and target: {e}")

    # Perform first split: training and temporary (validation + test)
    try:
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, 
            test_size=(test_size + val_size), 
            stratify=y, 
            random_state=random_state
        )
    except Exception as e:
        raise RuntimeError(f"Error during initial train/temp split: {e}")

    # Perform second split: validation and test from the temporary set
    try:
        # Calculate test proportion relative to temp
        relative_test_size = test_size / (test_size + val_size)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, 
            test_size=relative_test_size, 
            stratify=y_temp, 
            random_state=random_state
        )
    except Exception as e:
        raise RuntimeError(f"Error during validation/test split: {e}")

    # Ensure output directory exists
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        raise IOError(f"Could not create output directory {output_dir}: {e}")

    # Save datasets with error handling
    try:
        X_train.to_csv(os.path.join(output_dir, "X_train.csv"), index=False)
        X_val.to_csv(os.path.join(output_dir, "X_val.csv"), index=False)
        X_test.to_csv(os.path.join(output_dir, "X_test.csv"), index=False)
        y_train.to_csv(os.path.join(output_dir, "y_train.csv"), index=False)
        y_val.to_csv(os.path.join(output_dir, "y_val.csv"), index=False)
        y_test.to_csv(os.path.join(output_dir, "y_test.csv"), index=False)
    except Exception as e:
        raise IOError(f"Error saving split datasets: {e}")

    print(f"✅ Data Split Complete. Files saved to: {output_dir}")
    print(f"🔹 Training Set: {X_train.shape} features, {y_train.shape} target")
    print(f"🔹 Validation Set: {X_val.shape} features, {y_val.shape} target")
    print(f"🔹 Test Set: {X_test.shape} features, {y_test.shape} target")

from sklearn.model_selection import train_test_split