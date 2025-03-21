import os
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_train(input_path, output_path, model_dir, target_col="Target"):
    """
    Preprocess the training (or refined) dataset:
      - Reads the dataset.
      - Drops constant columns.
      - Separates target if available.
      - Fits LabelEncoders for categorical features.
      - Fits StandardScaler for numerical features.
      - Saves the fitted encoders and scaler.
      - Transforms and saves the preprocessed dataset.
      
    Parameters:
        input_path (str): Path to the raw/refined CSV file.
        output_path (str): Path to save the processed CSV.
        model_dir (str): Directory to save the fitted transformers.
        target_col (str): Name of the target column.
      
    Returns:
        pd.DataFrame: Preprocessed dataset.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError(f"The input file {input_path} is empty.")
    
    # Save original index to restore order later
    df["Original_Index"] = df.index

    # Drop constant columns
    constant_cols = df.columns[df.nunique() <= 1].tolist()
    if constant_cols:
        print(f"ℹ️ Dropping constant columns: {constant_cols}")
    df = df.loc[:, df.nunique() > 1]

    # Separate target if present
    if target_col in df.columns:
        y = df[target_col]
        df = df.drop(columns=[target_col])
    else:
        print(f"⚠️ Target column '{target_col}' not found. Proceeding without separating target.")
        y = None

    # Identify categorical and numerical features
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # Fit and transform categorical features
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    # Fit and transform numerical features
    scaler = None
    if num_cols:
        scaler = StandardScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])
    else:
        print("⚠️ No numerical columns found for scaling.")

    # Reattach target if present
    if y is not None:
        try:
            y = y.map({"Graduate": 1, "Dropout": 0}).fillna(-1).astype(int)
        except Exception as e:
            raise RuntimeError(f"Error processing the target column: {e}")
        df[target_col] = y

    # Restore original order
    df = df.sort_values("Original_Index").drop(columns=["Original_Index"])

    # Save the preprocessed dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Preprocessed dataset saved to {output_path}")

    # Save model artifacts (encoders and scaler)
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, "label_encoders.pkl"), "wb") as f:
        pickle.dump(encoders, f)
    if scaler is not None:
        with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
            pickle.dump(scaler, f)
    print(f"📁 Encoders and scaler saved to {model_dir}")

    return df

def preprocess_new(input_path, output_path, model_dir, target_col=None):
    """
    Preprocess a new dataset (e.g., enrolled data) using the pre-fitted transformers.
    This function:
      - Loads the dataset.
      - Loads the fitted encoders and scaler from model_dir.
      - Applies the same transformations to the new data.
      - Saves the transformed dataset.
      
    Parameters:
        input_path (str): Path to the new dataset CSV.
        output_path (str): Path to save the processed CSV.
        model_dir (str): Directory from which to load the fitted transformers.
        target_col (str or None): Name of the target column, if present.
                                   If None, no target processing is done.
      
    Returns:
        pd.DataFrame: Preprocessed new dataset.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError(f"The input file {input_path} is empty.")
    
    # Save original index
    df["Original_Index"] = df.index

    # Drop constant columns (using same logic as training data)
    constant_cols = df.columns[df.nunique() <= 1].tolist()
    if constant_cols:
        print(f"ℹ️ Dropping constant columns: {constant_cols}")
    df = df.loc[:, df.nunique() > 1]

    # If target_col is provided and exists, drop it (since new data likely has no target)
    if target_col and target_col in df.columns:
        df = df.drop(columns=[target_col])
    
    # Identify categorical and numerical columns
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # Load pre-fitted encoders
    encoders_path = os.path.join(model_dir, "label_encoders.pkl")
    if not os.path.exists(encoders_path):
        raise FileNotFoundError(f"Encoders file not found: {encoders_path}")
    with open(encoders_path, "rb") as f:
        encoders = pickle.load(f)

    # Apply encoders to categorical columns
    for col in cat_cols:
        if col in encoders:
            # If a new category is encountered, use the encoder's classes_
            le = encoders[col]
            # Map values; unknown categories can be assigned a special value (e.g., -1)
            df[col] = df[col].astype(str).apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        else:
            # If encoder not available, warn and try to convert to numeric if possible
            print(f"⚠️ No encoder found for column: {col}. Attempting to convert to numeric.")
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(-1).astype(int)

    # Load pre-fitted scaler
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    if num_cols:
        df[num_cols] = scaler.transform(df[num_cols])
    else:
        print("⚠️ No numerical columns found for scaling.")

    # Restore original order
    df = df.sort_values("Original_Index").drop(columns=["Original_Index"])

    # Save the processed new dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ New preprocessed dataset saved to {output_path}")

    return df
