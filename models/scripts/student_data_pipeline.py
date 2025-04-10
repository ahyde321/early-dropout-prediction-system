import os
import sys
import pandas as pd
import uuid
from faker import Faker

# === Setup ===
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
MODELS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(MODELS_DIR, ".."))
SYSTEM_UTILS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "system"))
if SYSTEM_UTILS_DIR not in sys.path:
    sys.path.append(SYSTEM_UTILS_DIR)

sys.path.append(ROOT_DIR)

from models.path_config import RAW_DIR
from data.data_loader import load_data
from data.data_imputer import apply_mice_imputation
from data.data_cleaner import clean_data, separate_enrolled_students
from data.data_aligner import align_datasets_and_combine
from formatting import to_snake_case

fake = Faker()

# === Load and Clean ===
raw_dataset1 = os.path.join(RAW_DIR, "raw_dataset1.csv")
raw_dataset2 = os.path.join(RAW_DIR, "raw_dataset2.csv")

try:
    df1, df2 = load_data(raw_dataset1, raw_dataset2)
    df1.columns = [to_snake_case(col) for col in df1.columns]
    df2.columns = [to_snake_case(col) for col in df2.columns]
    print(f"🔍 Loaded: df1={df1.shape}, df2={df2.shape}")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    sys.exit(1)

try:
    df1 = clean_data(df1)
    df2 = clean_data(df2)
    print(f"🧹 Cleaned: df1={df1.shape}, df2={df2.shape}")
except Exception as e:
    print(f"❌ Error cleaning data: {e}")
    sys.exit(1)

# === Align and Impute ===
try:
    combined_df = align_datasets_and_combine(df1, df2, ["admission_grade", "previous_qualification_grade"])
    print(f"✅ Combined: {combined_df.shape}")
    print(f"📋 Combined shape: {combined_df.shape}")
except Exception as e:
    print(f"❌ Error during dataset combining: {e}")
    sys.exit(1)

try:
    imputed_df = apply_mice_imputation(combined_df, ["admission_grade", "previous_qualification_grade"])
    print(f"📈 Imputed: {imputed_df.shape}")
except Exception as e:
    print(f"❌ Error during imputation: {e}")
    sys.exit(1)

# === Extract Enrolled Students from Combined Imputed ===
try:
    enrolled_df = separate_enrolled_students(
        combined_df=imputed_df,
        enrolled_path=None,  # we will not save intermediate
        filtered_path=None   # we will not save intermediate
    )
    print(f"🚀 Extracted Enrolled Students: {enrolled_df.shape}")
except Exception as e:
    print(f"❌ Error extracting enrolled students: {e}")
    sys.exit(1)

# === Add Names & Student Numbers ===
def generate_student_id():
    return str(uuid.uuid4())[:8]

enrolled_df["student_number"] = [generate_student_id() for _ in range(len(enrolled_df))]
enrolled_df["first_name"] = [fake.first_name() for _ in range(len(enrolled_df))]
enrolled_df["last_name"] = [fake.last_name() for _ in range(len(enrolled_df))]

# === Define Phase Field Sets ===
EARLY_FIELDS = [
    "student_number", "first_name", "last_name", "age_at_enrollment", "application_order",
    "curricular_units_1st_sem_enrolled", "daytime_evening_attendance", "debtor", "displaced",
    "gender", "marital_status", "scholarship_holder", "tuition_fees_up_to_date"
]

MID_FIELDS = [
    "student_number", "curricular_units_1st_sem_approved", "curricular_units_1st_sem_grade"
]

FINAL_FIELDS = ["student_number", "curricular_units_2nd_sem_grade"]

# === Create Output Directory ===
output_dir = os.path.join(MODELS_DIR, "data/enrolled")
os.makedirs(output_dir, exist_ok=True)

# === Export Phase Files ===
def save_phase_df(df, fields, name):
    phase_path = os.path.join(output_dir, f"enriched_enrolled_{name}.csv")
    filtered = df[[col for col in fields if col in df.columns]]
    try:
        filtered.to_csv(phase_path, index=False)
        print(f"✅ Saved {name.capitalize()} phase dataset to: {phase_path}")
    except Exception as e:
        print(f"❌ Error saving {name} data: {e}")

save_phase_df(enrolled_df, EARLY_FIELDS, "early")
save_phase_df(enrolled_df, MID_FIELDS, "mid")
save_phase_df(enrolled_df, FINAL_FIELDS, "final")