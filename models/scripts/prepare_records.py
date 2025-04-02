import os
import sys
import pandas as pd

# ➕ Add models/utils to sys.path before importing
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UTILS_DIR = os.path.join(MODELS_DIR, "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from student_record_preparer import process_student_upload  # ✅ Now works

# 📁 Input/output paths
INPUT_FILE = os.path.join(MODELS_DIR, "final", "data", "refined", "aligned_enrolled_pupils.csv")
OUTPUT_FILE = os.path.join(MODELS_DIR, "data", "enrolled", "final_prepared_enrolled_pupils.csv")

print("[INFO] Loading dataset...")
df = pd.read_csv(INPUT_FILE)

print("[INFO] Running preprocessing pipeline...")
df_clean = process_student_upload(df)

print("[INFO] Saving processed dataset...")
df_clean.to_csv(OUTPUT_FILE, index=False)

print(f"[DONE] Processed file saved as: {OUTPUT_FILE}")
