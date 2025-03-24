import pandas as pd
from pathlib import Path

def load_data(file_path1, file_path2):
    """
    Loads two datasets from CSV files and returns them as pandas DataFrames.

    Parameters:
        file_path1 (str or Path): File path for the first CSV file.
        file_path2 (str or Path): File path for the second CSV file.

    Returns:
        tuple: (df1, df2) DataFrames loaded from the provided CSV files.

    Raises:
        FileNotFoundError: If either file does not exist.
        ValueError: For issues with empty files or parsing errors.
        Exception: For any unexpected errors.
    """
    # Convert file paths to Path objects for better handling
    file_path1 = Path(file_path1)
    file_path2 = Path(file_path2)
    
    # Check if the files exist
    if not file_path1.exists():
        raise FileNotFoundError(f"File not found: {file_path1}")
    if not file_path2.exists():
        raise FileNotFoundError(f"File not found: {file_path2}")

    try:
        df1 = pd.read_csv(file_path1)
        df2 = pd.read_csv(file_path2)
    except pd.errors.EmptyDataError as e:
        raise ValueError(f"One of the files is empty: {e}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred while loading files: {e}")

    # Log warnings if the dataframes are empty
    if df1.empty:
        print(f"Warning: The file {file_path1} loaded an empty DataFrame.")
    if df2.empty:
        print(f"Warning: The file {file_path2} loaded an empty DataFrame.")
        
    return df1, df2
