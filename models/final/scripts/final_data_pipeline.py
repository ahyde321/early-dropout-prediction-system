import os
import sys

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
from data.data_aligner import align_datasets_and_combine, align_enrolled_pupils
from data.data_preprocessor import preprocess_train, preprocess_new
from data.data_splitter import split_train_val_test
from formatting import to_snake_case

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
    print(f"🧹 Cleaned: df1={df1.shape}, df2={df2.shape}")
except Exception as e:
    print(f"Error during data cleaning: {e}")
    sys.exit(1)

# === Step 2: Align & Impute ===
try:
    combined_df = align_datasets_and_combine(df1, df2, ["admission_grade", "previous_qualification_grade"])
    print(f"✅ Combined: {combined_df.shape}")
except Exception as e:
    print(f"Error during dataset alignment: {e}")
    sys.exit(1)

try:
    imputed_df = apply_mice_imputation(combined_df, ["admission_grade", "previous_qualification_grade"])
    print(f"📈 Imputed: {imputed_df.shape}")
except Exception as e:
    print(f"Error during imputation: {e}")
    sys.exit(1)

# === Step 3: Separate Enrolled & Past Pupils ===
try:
    past_pupils_df = separate_enrolled_students(
        combined_df=imputed_df,
        enrolled_path=os.path.join(FILTERED_DIR, "enrolled_pupils.csv"),
        filtered_path=os.path.join(FILTERED_DIR, "past_pupils.csv")
    )
    print(f"🚀 Past Pupils: {past_pupils_df.shape}")
except Exception as e:
    print(f"Error during separation of enrolled students: {e}")
    sys.exit(1)

# === Step 4: Feature Engineering ===
try:
    past_pupils_df_reduced = remove_highly_correlated_features(past_pupils_df)
    print(f"🔍 Dataset shape after removing correlated features: {past_pupils_df_reduced.shape}")
except Exception as e:
    print(f"Error during removal of correlated features: {e}")
    sys.exit(1)

try:
    final_dataset = select_best_features(past_pupils_df_reduced, target_column="target", importance_threshold=0.95)
    print(f"✅ Final Dataset shape after feature selection: {final_dataset.shape}")
except Exception as e:
    print(f"Error during feature selection: {e}")
    sys.exit(1)

try:
    refined_past_path = os.path.join(REFINED_DIR, "refined_past_pupil_dataset.csv")
    final_dataset.to_csv(refined_past_path, index=False)
    print(f"✅ Refined dataset saved at: {refined_past_path}")
except Exception as e:
    print(f"Error saving refined dataset: {e}")
    sys.exit(1)

try:
    aligned_enrolled_df = align_enrolled_pupils(
        enrolled_path=os.path.join(FILTERED_DIR, "enrolled_pupils.csv"),
        final_dataset=final_dataset,
        output_path=os.path.join(REFINED_DIR, "aligned_enrolled_pupils.csv")
    )
    print(f"✅ Aligned enrolled pupils dataset shape: {aligned_enrolled_df.shape}")
except Exception as e:
    print(f"Error during enrolled pupils alignment: {e}")
    sys.exit(1)

# ✅ Step 5: Preprocess for Random Forest
preprocessed_past_path = os.path.join(PREPROCESSED_DIR, "preprocessed_past_pupils.csv")
try:
    preprocess_train(
        input_path=refined_past_path,
        output_path=preprocessed_past_path,
        model_dir=ARTIFACTS_DIR,
        target_col="target"
    )
    print(f"✅ Preprocessed past pupils dataset saved to: {preprocessed_past_path}")
except Exception as e:
    print(f"Error during preprocessing training data: {e}")
    sys.exit(1)

preprocessed_enrolled_path = os.path.join(PREPROCESSED_DIR, "preprocessed_enrolled_pupils.csv")
try:
    preprocess_new(
        input_path=os.path.join(REFINED_DIR, "aligned_enrolled_pupils.csv"),
        output_path=preprocessed_enrolled_path,
        model_dir=ARTIFACTS_DIR,
        target_col="target"
    )
    print(f"✅ Preprocessed enrolled pupils dataset saved to: {preprocessed_enrolled_path}")
except Exception as e:
    print(f"Error during preprocessing enrolled data: {e}")
    sys.exit(1)

# === Step 6: Train/Val/Test Split ===
try:
    if not os.path.exists(preprocessed_past_path):
        raise FileNotFoundError(f"Preprocessed past dataset not found: {preprocessed_past_path}")

    split_train_val_test(
        input_path=preprocessed_past_path,
        output_dir=READY_DIR
    )
    print(f"✅ Train/Val/Test split completed. Files saved to: {READY_DIR}")
except Exception as e:
    print(f"Error during train/val/test split: {e}")
    sys.exit(1)

print("✅ Data pipeline completed successfully!")
