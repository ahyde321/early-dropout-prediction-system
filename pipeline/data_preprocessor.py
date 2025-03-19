import os
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(input_path, output_path, model_dir):
    """
    Preprocess the dataset for Random Forest training.
    
    Steps:
    1. Encode categorical features.
    2. Scale numerical features (optional).
    3. Save encoders and scalers for consistency.

    Parameters:
    - input_path (str): Path to the dataset to be preprocessed.
    - output_path (str): Path to save the processed dataset.
    - model_dir (str): Directory to save encoding/scaling weights.

    Returns:
    - pd.DataFrame: Preprocessed dataset.
    """

    # Load dataset
    df = pd.read_csv(input_path)

    # Define categorical and numerical features
    categorical_features = ["Application mode", "Debtor", "Gender", "Scholarship holder", "Tuition fees up to date"]
    numerical_features = ["Age at enrollment", "Curricular units 1st sem (approved)", 
                          "Curricular units 1st sem (enrolled)", "Curricular units 1st sem (grade)", 
                          "Curricular units 2nd sem (grade)"]
    
    # Encode categorical features
    encoders = {}
    for col in categorical_features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    # Convert Target column to binary (1 = Enrolled, 0 = Dropped)
    df["Target"] = df["Target"].apply(lambda x: 1 if x == "Enrolled" else 0)

    # Scale numerical features (optional)
    scaler = StandardScaler()
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    # Save encoders and scalers
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, "encoders.pkl"), "wb") as f:
        pickle.dump(encoders, f)
    with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    # Save the preprocessed dataset
    df.to_csv(output_path, index=False)

    print(f"✅ Preprocessed dataset saved to: {output_path}")
    print(f"📂 Encoders and scaler saved in: {model_dir}")

    return df