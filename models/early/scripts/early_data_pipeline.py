import os
import sys
import pandas as pd

EARLY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(EARLY_DIR)

# === Setup ===
from path_config import (
    RAW_DIR, FILTERED_DIR, REFINED_DIR, PREPROCESSED_DIR, READY_DIR, ARTIFACTS_DIR
)

from data.data_loader import load_data
from data.data_imputer import apply_mice_imputation
from data.data_cleaner import clean_data
from data.feature_selector import remove_highly_correlated_features, select_best_features
from data.data_aligner import align_datasets_and_combine
from data.data_preprocessor import preprocess_train
from data.data_splitter import split_train_val_test
from formatting import to_snake_case

EXCLUDE_COLS = [
    "curricular_units_1st_sem_evaluations",
    "curricular_units_1st_sem_approved",
    "curricular_units_1st_sem_grade",
    "curricular_units_1st_sem_without_evaluations",
    "curricular_units_2nd_sem_evaluations",
    "curricular_units_2nd_sem_approved",
    "curricular_units_2nd_sem_grade",
    "curricular_units_2nd_sem_without_evaluations"
]

# === Step 1: Load and Clean Data ===
raw_dataset1 = os.path.join(RAW_DIR, "raw_dataset1.csv")
raw_dataset2 = os.path.join(RAW_DIR, "raw_dataset2.csv")

try:
    df1, df2 = load_data(raw_dataset1, raw_dataset2)
    df1.columns = [to_snake_case(col) for col in df1.columns]
    df2.columns = [to_snake_case(col) for col in df2.columns]
    print(f"🔍 Loaded: df1={df1.shape}, df2={df2.shape}")
except Exception as e:
    print(f"Error during data loading: {e}")
    sys.exit(1)

try:
    df1 = clean_data(df1)
    df2 = clean_data(df2)
    df1 = df1.drop(columns=[col for col in EXCLUDE_COLS if col in df1.columns], errors='ignore')
    df2 = df2.drop(columns=[col for col in EXCLUDE_COLS if col in df2.columns], errors='ignore')
    print(f"🧹 Cleaned + Filtered: df1={df1.shape}, df2={df2.shape}")
except Exception as e:
    print(f"Error during data cleaning: {e}")
    sys.exit(1)

# === Step 2: Align & Impute ===
try:
    combined_df = align_datasets_and_combine(df1, df2, [])
    print(f"✅ Combined: {combined_df.shape}")
except Exception as e:
    print(f"Error during dataset alignment: {e}")
    sys.exit(1)

try:
    combined_df = combined_df[combined_df["target"] != "Enrolled"]
    combined_df = combined_df.reset_index(drop=True)
    print(f"🚫 Dropped enrolled students: {combined_df.shape}")
except Exception as e:
    print(f"Error filtering enrolled students: {e}")
    sys.exit(1)

try:
    imputed_df = apply_mice_imputation(combined_df, ["admission_grade", "previous_qualification_grade"])
    print(f"📈 Imputed: {imputed_df.shape}")
except Exception as e:
    print(f"Error during imputation: {e}")
    sys.exit(1)

# === Step 3: Feature Engineering ===
try:
    reduced_df = remove_highly_correlated_features(imputed_df)
    print(f"🔍 After removing correlated features: {reduced_df.shape}")
except Exception as e:
    print(f"Error during feature reduction: {e}")
    sys.exit(1)

try:
    final_dataset = select_best_features(reduced_df, target_column="target", importance_threshold=0.95)
    print(f"✅ Final feature selection result: {final_dataset.shape}")
except Exception as e:
    print(f"Error during feature selection: {e}")
    sys.exit(1)

# === Step 4: Save Refined Data ===
try:
    refined_path = os.path.join(REFINED_DIR, "refined_past_pupil_dataset.csv")
    final_dataset.to_csv(refined_path, index=False)
    print(f"✅ Refined dataset saved at: {refined_path}")
except Exception as e:
    print(f"Error saving refined dataset: {e}")
    sys.exit(1)

# === Step 5: Preprocessing ===
preprocessed_path = os.path.join(PREPROCESSED_DIR, "preprocessed_past_pupils.csv")
try:
    preprocess_train(
        input_path=refined_path,
        output_path=preprocessed_path,
        model_dir=ARTIFACTS_DIR,
        target_col="target"
    )
    print(f"✅ Preprocessed dataset saved to: {preprocessed_path}")
except Exception as e:
    print(f"Error during preprocessing: {e}")
    sys.exit(1)

# === Step 6: Train/Val/Test Split ===
try:
    if not os.path.exists(preprocessed_path):
        raise FileNotFoundError(f"Preprocessed dataset not found: {preprocessed_path}")

    split_train_val_test(
        input_path=preprocessed_path,
        output_dir=READY_DIR
    )
    print(f"✅ Train/Val/Test split completed. Files saved to: {READY_DIR}")
except Exception as e:
    print(f"Error during train/val/test split: {e}")
    sys.exit(1)

print("✅ Early Dropout Data Pipeline completed successfully!")