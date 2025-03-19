import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_val_test(input_path, output_dir, test_size=0.15, val_size=0.15, random_state=42):
    """
    Splits the dataset into training, validation, and test sets before preprocessing.

    Parameters:
    - input_path (str): Path to the dataset (past pupils dataset).
    - output_dir (str): Directory to save the split datasets.
    - test_size (float): Proportion of data for the test set.
    - val_size (float): Proportion of data for the validation set.
    - random_state (int): Random seed for reproducibility.

    Returns:
    - None (Saves train, validation, and test datasets as CSV files)
    """

    # Load dataset
    df = pd.read_csv(input_path)

    # Separate features and target
    X = df.drop(columns=["Target"])
    y = df["Target"]

    # Split into training and temp (validation + test)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=(test_size + val_size), stratify=y, random_state=random_state
    )

    # Split temp into validation and test sets
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=test_size / (test_size + val_size), stratify=y_temp, random_state=random_state
    )

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save datasets
    X_train.to_csv(os.path.join(output_dir, "X_train.csv"), index=False)
    X_val.to_csv(os.path.join(output_dir, "X_val.csv"), index=False)
    X_test.to_csv(os.path.join(output_dir, "X_test.csv"), index=False)

    y_train.to_csv(os.path.join(output_dir, "y_train.csv"), index=False)
    y_val.to_csv(os.path.join(output_dir, "y_val.csv"), index=False)
    y_test.to_csv(os.path.join(output_dir, "y_test.csv"), index=False)

    print(f"✅ Data Split Complete. Saved to: {output_dir}")
    print(f"🔹 Training Set: {X_train.shape}, {y_train.shape}")
    print(f"🔹 Validation Set: {X_val.shape}, {y_val.shape}")
    print(f"🔹 Test Set: {X_test.shape}, {y_test.shape}")
