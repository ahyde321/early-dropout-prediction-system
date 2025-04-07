import os
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_row_for_inference(data: dict, model_dir: str) -> pd.DataFrame:
    df = pd.DataFrame([data])

    # 🧹 Drop columns that should never be part of prediction
    df = df.drop(columns=["target", "original_index"], errors="ignore")

    # Identify column types
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    num_cols = df.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()

    # 🔄 Apply label encoders
    encoders_path = os.path.join(model_dir, "label_encoders.pkl")
    with open(encoders_path, "rb") as f:
        encoders = pickle.load(f)

    for col in cat_cols:
        if col in encoders:
            le = encoders[col]
            df[col] = df[col].astype(str).apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(-1).astype(int)

    # 🔄 Apply scaler
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    if num_cols:
        df[num_cols] = scaler.transform(df[num_cols])

    # ✅ Reorder and match features exactly
    feature_list_path = os.path.join(model_dir, "feature_names.pkl")
    if os.path.exists(feature_list_path):
        with open(feature_list_path, "rb") as f:
            expected_cols = pickle.load(f)

        # Add missing columns with 0, drop extras
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_cols]

    return df
