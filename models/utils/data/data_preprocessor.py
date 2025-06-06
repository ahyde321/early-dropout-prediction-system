import os
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_train(input_path, output_path, model_dir, target_col="target"):
    """
    Preprocess the training dataset:
      - Reads the dataset.
      - Drops constant columns.
      - Separates and encodes target if available.
      - Fits LabelEncoders for categorical features.
      - Fits StandardScaler for numerical features.
      - Saves encoders, scaler, and feature list.
      - Transforms and saves the preprocessed dataset.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError(f"The input file {input_path} is empty.")

    # Drop constant columns
    constant_cols = df.columns[df.nunique() <= 1].tolist()
    df = df.loc[:, df.nunique() > 1]

    # Separate target if present
    y = None
    if target_col in df.columns:
        y = df[target_col]
        df = df.drop(columns=[target_col])

    # Identify categorical and numerical features
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # Encode categorical features
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    # Scale numerical features
    scaler = None
    if num_cols:
        scaler = StandardScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])

    # Save preprocessing artifacts
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, "label_encoders.pkl"), "wb") as f:
        pickle.dump(encoders, f)
    if scaler is not None:
        with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
            pickle.dump(scaler, f)
    with open(os.path.join(model_dir, "feature_names.pkl"), "wb") as f:
        pickle.dump(df.columns.tolist(), f)

    # Reattach and encode target if present
    if y is not None:
        y = y.map({"Graduate": 1, "Dropout": 0}).fillna(-1).astype(int)
        df[target_col] = y

    # Save preprocessed dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    return df

def preprocess_new(input_path, output_path, model_dir, target_col="target"):
    """
    Preprocess new (unseen) student data (e.g. enrolled pupils):
      - Reads the input dataset
      - Loads existing encoders, scaler, and feature list
      - Applies same transformations used during training
      - Outputs aligned, preprocessed dataset ready for prediction
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError(f"The input file {input_path} is empty.")

    # Load preprocessing artifacts
    with open(os.path.join(model_dir, "label_encoders.pkl"), "rb") as f:
        encoders = pickle.load(f)
    with open(os.path.join(model_dir, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    with open(os.path.join(model_dir, "feature_names.pkl"), "rb") as f:
        feature_names = pickle.load(f)

    # Encode categorical columns
    for col, le in encoders.items():
        if col in df.columns:
            df[col] = df[col].astype(str).map(lambda x: x if x in le.classes_ else "__unknown__")
            if "__unknown__" not in le.classes_:
                le.classes_ = list(le.classes_) + ["__unknown__"]
            df[col] = le.transform(df[col])

    # Scale numerical columns
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    if scaler and num_cols:
        df[num_cols] = scaler.transform(df[num_cols])

    # Ensure all expected columns are present
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0  # Fill missing expected columns
    df = df[feature_names]  # Align column order

    # Save preprocessed output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    return df