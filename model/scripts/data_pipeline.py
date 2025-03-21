import os
import sys
# === Setup ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from utils.data_loader import load_data
from utils.data_imputer import apply_mice_imputation
from utils.data_cleaner import clean_data, separate_enrolled_students
from utils.feature_selector import remove_highly_correlated_features, select_best_features
from utils.data_aligner import align_datasets_and_combine, align_enrolled_pupils
from utils.data_preprocessor import preprocess_train, preprocess_new
from utils.data_splitter import split_train_val_test

RAW_DIR = os.path.join(BASE_DIR, "data/raw")
FILTERED_DIR = os.path.join(BASE_DIR, "data/filtered")
REFINED_DIR = os.path.join(BASE_DIR, "data/refined")
PREPROCESSED_DIR = os.path.join(BASE_DIR, "data/preprocessed")
READY_DIR = os.path.join(BASE_DIR, "data/ready")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(PREPROCESSED_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# === Step 1: Load and Clean Data ===
# Define your raw data file paths
raw_dataset1 = os.path.join(RAW_DIR, "raw_dataset1.csv")
raw_dataset2 = os.path.join(RAW_DIR, "raw_dataset2.csv")

# Attempt to load data with improved error handling
try:
    df1, df2 = load_data(raw_dataset1, raw_dataset2)
    print(f"🔍 Loaded: df1={df1.shape}, df2={df2.shape}")
except Exception as e:
    print(f"Error during data loading: {e}")
    sys.exit(1)  # Optionally exit if loading fails

# Clean data
try:
    df1 = clean_data(df1)
    df2 = clean_data(df2)
    print(f"🧹 Cleaned: df1={df1.shape}, df2={df2.shape}")
except Exception as e:
    print(f"Error during data cleaning: {e}")
    sys.exit(1)

# Step 2: Align & Impute
try:
    combined_df = align_datasets_and_combine(df1, df2, ["Admission grade", "Previous qualification (grade)"])
    print(f"✅ Combined: {combined_df.shape}")
except Exception as e:
    print(f"Error during dataset alignment: {e}")
    sys.exit(1)

try:
    imputed_df = apply_mice_imputation(combined_df, ["Admission grade", "Previous qualification (grade)"])
    print(f"📈 Imputed: {imputed_df.shape}")
except Exception as e:
    print(f"Error during imputation: {e}")
    sys.exit(1)

# === Step 3: Separate Enrolled & Past Pupils ===
filtered_dir = os.path.join(BASE_DIR, "data/filtered")
try:
    past_pupils_df = separate_enrolled_students(
        combined_df=imputed_df,  # assuming imputed_df is available from previous steps
        enrolled_path=os.path.join(filtered_dir, "enrolled_pupils.csv"),
        filtered_path=os.path.join(filtered_dir, "past_pupils.csv")
    )
    print(f"🚀 Past Pupils: {past_pupils_df.shape}")
except Exception as e:
    print(f"Error during separation of enrolled students: {e}")
    sys.exit(1)

# === Step 4: Feature Engineering ===
try:
    # Remove highly correlated features first
    past_pupils_df_reduced = remove_highly_correlated_features(past_pupils_df)
    print(f"🔍 Dataset shape after removing correlated features: {past_pupils_df_reduced.shape}")
except Exception as e:
    print(f"Error during removal of correlated features: {e}")
    sys.exit(1)

try:
    # Select best features dynamically
    final_dataset = select_best_features(past_pupils_df_reduced, target_column="Target", importance_threshold=0.95)
    print(f"✅ Final Dataset shape after feature selection: {final_dataset.shape}")
except Exception as e:
    print(f"Error during feature selection: {e}")
    sys.exit(1)

# Save refined dataset
try:
    refined_past_path = os.path.join(REFINED_DIR, "refined_past_pupil_dataset.csv")
    final_dataset.to_csv(refined_past_path, index=False)
    print(f"✅ Refined dataset saved at: {refined_past_path}")
except Exception as e:
    print(f"Error saving refined dataset: {e}")
    sys.exit(1)

# Align enrolled to final features
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


# === Step 5: Preprocess for Random Forest ===

# Preprocess the refined past pupils dataset (training)
preprocessed_past_path = os.path.join(PREPROCESSED_DIR, "preprocessed_past_pupils.csv")
try:
    preprocessed_past_pupils = preprocess_train(
        input_path=refined_past_path,
        output_path=preprocessed_past_path,
        model_dir=MODEL_DIR,
        target_col="Target"
    )
    print(f"✅ Preprocessed past pupils dataset saved to: {preprocessed_past_path}")
except Exception as e:
    print(f"Error during preprocessing training data: {e}")
    sys.exit(1)

# Preprocess the enrolled pupils dataset (new data) using the same transformers
preprocessed_enrolled_path = os.path.join(PREPROCESSED_DIR, "preprocessed_enrolled_pupils.csv")
try:
    preprocessed_enrolled_pupils = preprocess_new(
        input_path=os.path.join(REFINED_DIR, "aligned_enrolled_pupils.csv"),
        output_path=preprocessed_enrolled_path,
        model_dir=MODEL_DIR,
        target_col="Target"  # or None if enrolled data does not have a target column
    )
    print(f"✅ Preprocessed enrolled pupils dataset saved to: {preprocessed_enrolled_path}")
except Exception as e:
    print(f"Error during preprocessing enrolled data: {e}")
    sys.exit(1)

# === Step 6: Train/Val/Test Split ===
try:
    # Confirm that the preprocessed past dataset exists before splitting
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
