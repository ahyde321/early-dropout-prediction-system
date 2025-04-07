import os
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_train(input_path, output_path, model_dir, target_col="target"):
    """
    Preprocess the training (or refined) dataset:
      - Reads the dataset.
      - Drops constant columns.
      - Separates target if available.
      - Fits LabelEncoders for categorical features.
      - Fits StandardScaler for numerical features.
      - Saves the fitted encoders and scaler.
      - Transforms and saves the preprocessed dataset.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError(f"The input file {input_path} is empty.")
    
    # Save original index to restore order later
    df["original_index"] = df.index

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

    # 🧹 Restore original order and drop 'original_index' early — before transformation
    df = df.sort_values("original_index").drop(columns=["original_index"], errors="ignore")

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

    # ✅ Save model artifacts BEFORE reattaching the target
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, "label_encoders.pkl"), "wb") as f:
        pickle.dump(encoders, f)
    if scaler is not None:
        with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
            pickle.dump(scaler, f)
    with open(os.path.join(model_dir, "feature_names.pkl"), "wb") as f:
        pickle.dump(df.columns.tolist(), f)
    print(f"📁 Encoders, scaler, and clean feature list saved to {model_dir}")

    # ✅ Now reattach the target if needed
    if y is not None:
        try:
            y = y.map({"Graduate": 1, "Dropout": 0}).fillna(-1).astype(int)
        except Exception as e:
            raise RuntimeError(f"Error processing the target column: {e}")
        df[target_col] = y

    # Save the preprocessed dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Preprocessed dataset saved to {output_path}")

    return df


def preprocess_new(input_path, output_path, model_dir, target_col=None):
    """
    Preprocess a new dataset (e.g., enrolled data) using the pre-fitted transformers.
    Applies the same transformations as training.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError(f"The input file {input_path} is empty.")
    
    # Save original index for sorting (but will drop later)
    df["original_index"] = df.index

    # Drop constant columns
    constant_cols = df.columns[df.nunique() <= 1].tolist()
    if constant_cols:
        print(f"ℹ️ Dropping constant columns: {constant_cols}")
    df = df.loc[:, df.nunique() > 1]

    # Drop target if present
    if target_col and target_col in df.columns:
        df = df.drop(columns=[target_col])

    # Drop original_index early so it's never passed to scaler
    df = df.drop(columns=["original_index"], errors="ignore")

    # Identify feature types
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # Load encoders
    encoders_path = os.path.join(model_dir, "label_encoders.pkl")
    if not os.path.exists(encoders_path):
        raise FileNotFoundError(f"Encoders file not found: {encoders_path}")
    with open(encoders_path, "rb") as f:
        encoders = pickle.load(f)

    # Apply encoders
    for col in cat_cols:
        if col in encoders:
            le = encoders[col]
            df[col] = df[col].astype(str).apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        else:
            print(f"⚠️ No encoder found for column: {col}. Attempting numeric conversion.")
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(-1).astype(int)

    # Load and apply scaler
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    if num_cols:
        df[num_cols] = scaler.transform(df[num_cols])
    else:
        print("⚠️ No numerical columns found for scaling.")

    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ New preprocessed dataset saved to {output_path}")

    return df


def preprocess_row_for_inference(data: dict, model_dir: str) -> pd.DataFrame:
    df = pd.DataFrame([data])

    # Identify types
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    num_cols = df.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()

    # Load encoders
    with open(os.path.join(model_dir, "label_encoders.pkl"), "rb") as f:
        encoders = pickle.load(f)

    for col in cat_cols:
        if col in encoders:
            le = encoders[col]
            df[col] = df[col].astype(str).apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(-1).astype(int)

    # Load scaler
    with open(os.path.join(model_dir, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)

    if num_cols:
        df[num_cols] = scaler.transform(df[num_cols])

    # 🧠 Load expected column order
    feature_path = os.path.join(model_dir, "feature_names.pkl")
    if os.path.exists(feature_path):
        with open(feature_path, "rb") as f:
            expected_cols = pickle.load(f)

        # Add missing cols with 0, drop extra, and reorder
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0  # or np.nan if you prefer
        df = df[expected_cols]

    return df


