import pandas as pd
from pathlib import Path

def load_data(file_path):
    """
    Loads a single dataset from a CSV file and returns it as a pandas DataFrame.

    Parameters:
        file_path (str or Path): File path for the CSV file.

    Returns:
        DataFrame: Loaded DataFrame from the provided CSV file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: For issues with empty files or parsing errors.
        Exception: For any unexpected errors.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as e:
        raise ValueError(f"The file is empty: {e}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred while loading the file: {e}")

    if df.empty:
        print(f"Warning: The file {file_path} loaded an empty DataFrame.")

    return df
