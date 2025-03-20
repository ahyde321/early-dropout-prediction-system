import os
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(input_path, output_path, model_dir):
    """
    Preprocess the dataset for Random Forest training while preserving row order.

    Steps:
    1. Preserve row order by adding an 'Original_Index'.
    2. Encode categorical features.
    3. Scale numerical features.
    4. Convert 'Target' column (if present) - Graduate → 1, Dropout → 0.
    5. Restore original order before saving.
    6. Save encoders and scalers for consistency.

    Parameters:
    - input_path (str): Path to the dataset to be preprocessed.
    - output_path (str): Path to save the processed dataset.
    - model_dir (str): Directory to save encoding/scaling weights.

    Returns:
    - pd.DataFrame: Preprocessed dataset.
    """

    # ✅ Load dataset and preserve original index
    df = pd.read_csv(input_path)
    df["Original_Index"] = df.index  # ✅ Store original index before processing

    # Define categorical and numerical features
    categorical_features = ["Application mode", "Debtor", "Gender", "Scholarship holder", "Tuition fees up to date"]
    numerical_features = ["Age at enrollment", "Curricular units 1st sem (approved)", 
                          "Curricular units 1st sem (enrolled)", "Curricular units 1st sem (grade)", 
                          "Curricular units 2nd sem (grade)"]

    # ✅ Ensure all categorical features exist (in case columns are missing)
    for col in categorical_features:
        if col not in df.columns:
            df[col] = "Unknown"

    # ✅ Encode categorical features
    encoders = {}
    for col in categorical_features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    # ✅ Convert 'Target' column: "Graduate" → 1, "Dropout" → 0 (if it exists)
    if "Target" in df.columns:
        df["Target"] = df["Target"].apply(lambda x: 1 if x == "Graduate" else 0)

    # ✅ Ensure all numerical features exist (avoid errors when scaling)
    for col in numerical_features:
        if col not in df.columns:
            df[col] = 0  # Fill missing numerical features with 0

    # ✅ Scale numerical features
    scaler = StandardScaler()
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    # ✅ Restore original order before saving
    df = df.sort_values("Original_Index").drop(columns=["Original_Index"])

    # ✅ Save encoders and scalers
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, "encoders.pkl"), "wb") as f:
        pickle.dump(encoders, f)
    with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    # ✅ Save the preprocessed dataset while ensuring row order remains the same
    df.to_csv(output_path, index=False)

    print(f"✅ Preprocessed dataset saved to: {output_path}")
    print(f"📂 Encoders and scaler saved in: {model_dir}")

    return df
