import pandas as pd

def load_data(file_path1, file_path2):
    """
    Loads two datasets and returns them as pandas DataFrames.
    """
    try:
        df1 = pd.read_csv(file_path1)
        df2 = pd.read_csv(file_path2)
        return df1, df2
    except Exception as e:
        raise FileNotFoundError(f"Error loading files: {e}")
