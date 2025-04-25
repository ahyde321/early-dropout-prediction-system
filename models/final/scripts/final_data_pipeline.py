import os
import sys
import pandas as pd

FINAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(FINAL_DIR)

# === Setup ===
from path_config import (
    RAW_DIR, FILTERED_DIR, REFINED_DIR, PREPROCESSED_DIR, READY_DIR, ARTIFACTS_DIR
)

from data.data_loader import load_data
from data.data_imputer import apply_mice_imputation
from data.data_cleaner import clean_data, separate_enrolled_students
from data.feature_selector import remove_highly_correlated_features, select_best_features
from data.data_aligner import align_enrolled_pupils
from data.data_preprocessor import preprocess_train, preprocess_new
from data.data_splitter import split_train_val_test
from formatting import to_snake_case

# === Step 1: Load and Clean Data ===
raw_dataset = os.path.join(RAW_DIR, "raw_dataset1.csv")

try:
    df = load_data(raw_dataset)
    df.columns = [to_snake_case(col) for col in df.columns]
    print(f"🔍 Loaded raw dataset: {df.shape}")
    print("🧪 Columns:", df.columns.tolist())
except Exception as e:
    print(f"❌ Error during data loading: {e}")
    sys.exit(1)

try:
    df = clean_data(df)
    print(f"🧹 Cleaned dataset: {df.shape}")
except Exception as e:
    print(f"❌ Error during data cleaning: {e}")
    sys.exit(1)

# === Step 2: Filter & Impute ===
try:
    df = df[df["target"] != "Enrolled"].reset_index(drop=True)
    print(f"🚫 Dropped 'Enrolled' students: {df.shape}")
    print("🧪 Target value counts after filtering:\n", df["target"].value_counts())
except Exception as e:
    print(f"❌ Error filtering enrolled students: {e}")
    sys.exit(1)

# try:
#     df = apply_mice_imputation(df, ["admission_grade", "previous_qualification_grade"])
#     print(f"📈 Imputed dataset shape: {df.shape}")
#     print("🧪 Null values remaining:\n", df.isnull().sum()[df.isnull().sum() > 0])
# except Exception as e:
#     print(f"❌ Error during imputation: {e}")
#     sys.exit(1)

# === Step 3: Feature Engineering ===
try:
    df_reduced = remove_highly_correlated_features(df)
    print(f"🔍 Dataset after removing correlated features: {df_reduced.shape}")
except Exception as e:
    print(f"❌ Error during removal of correlated features: {e}")
    sys.exit(1)

# Log numerical columns for diagnostics
numerical_cols = df_reduced.select_dtypes(include=['int64', 'float64']).columns
print("🧪 Numerical features detected:", numerical_cols.tolist())
print("🧪 Zero-variance features:", [col for col in numerical_cols if df_reduced[col].nunique() <= 1])

try:
    final_dataset = select_best_features(df_reduced, target_column="target", importance_threshold=0.95)
    print(f"✅ Final dataset after feature selection: {final_dataset.shape}")
except Exception as e:
    print(f"❌ Error during feature selection: {e}")
    sys.exit(1)

# === Step 4: Save Refined Dataset ===
try:
    refined_past_path = os.path.join(REFINED_DIR, "refined_past_pupil_dataset.csv")
    final_dataset.to_csv(refined_past_path, index=False)
    print(f"💾 Refined dataset saved at: {refined_past_path}")
except Exception as e:
    print(f"❌ Error saving refined dataset: {e}")
    sys.exit(1)

# === Step 5: Preprocess ===
preprocessed_past_path = os.path.join(PREPROCESSED_DIR, "preprocessed_past_pupils.csv")
try:
    preprocess_train(
        input_path=refined_past_path,
        output_path=preprocessed_past_path,
        model_dir=ARTIFACTS_DIR,
        target_col="target"
    )
    print(f"✅ Preprocessed training dataset saved to: {preprocessed_past_path}")
except Exception as e:
    print(f"❌ Error during preprocessing training data: {e}")
    sys.exit(1)

# === Step 6: Train/Val/Test Split ===
try:
    if not os.path.exists(preprocessed_past_path):
        raise FileNotFoundError(f"Preprocessed dataset not found: {preprocessed_past_path}")

    split_train_val_test(
        input_path=preprocessed_past_path,
        output_dir=READY_DIR
    )
    print(f"📁 Train/Val/Test split completed. Files saved to: {READY_DIR}")
    print("📄 Files in READY_DIR:", os.listdir(READY_DIR))
except Exception as e:
    print(f"❌ Error during train/val/test split: {e}")
    sys.exit(1)

print("✅ Final Dropout Data Pipeline completed successfully!")
