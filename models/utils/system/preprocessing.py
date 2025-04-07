import os
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_row_for_inference(data: dict, model_dir: str, model) -> pd.DataFrame:
    df = pd.DataFrame([data])

    # Drop unwanted columns
    df = df.drop(columns=["target", "original_index"], errors="ignore")

    # Use model's expected features
    expected_cols = list(model.feature_names_in_)

    # Add missing columns with default 0
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0

    # Drop extra columns and reorder
    df = df[expected_cols]

    # Identify categorical and numerical features
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    num_cols = df.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()

    # Load label encoders
    with open(os.path.join(model_dir, "label_encoders.pkl"), "rb") as f:
        encoders = pickle.load(f)

    for col in cat_cols:
        if col in encoders:
            le = encoders[col]
            df[col] = df[col].astype(str).apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(-1).astype(int)

    # Load and apply scaler
    with open(os.path.join(model_dir, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)

    if num_cols:
        df[num_cols] = scaler.transform(df[num_cols])

    return df
