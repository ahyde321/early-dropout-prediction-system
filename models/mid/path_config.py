import os
import sys

# 📁 Absolute path to the "final" directory
MID_DIR = os.path.dirname(os.path.abspath(__file__))

# 📁 Go up one level to get to "model"
MODEL_DIR = os.path.dirname(MID_DIR)

# 📁 Path to the shared "utils" directory
UTILS_DIR = os.path.join(MODEL_DIR, "utils")

# ➕ Add utils directory to sys.path so imports work
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# ➕ Add subdirectories of utils to sys.path
SYSTEM_UTILS_DIR = os.path.join(UTILS_DIR, "system")
DATA_UTILS_DIR = os.path.join(UTILS_DIR, "data")

if SYSTEM_UTILS_DIR not in sys.path:
    sys.path.append(SYSTEM_UTILS_DIR)

# 📂 Define key directories used across scripts/tests
DATA_DIR = os.path.join(MID_DIR, "data")
ARTIFACTS_DIR = os.path.join(MID_DIR, "artifacts")  # renamed from models
SCRIPTS_DIR = os.path.join(MID_DIR, "scripts")
TESTS_DIR = os.path.join(MID_DIR, "tests")

# 📂 Subdirectories for data pipeline
RAW_DIR = os.path.join(MODEL_DIR, "data", "raw")
FILTERED_DIR = os.path.join(DATA_DIR, "filtered")
REFINED_DIR = os.path.join(DATA_DIR, "refined")
PREPROCESSED_DIR = os.path.join(DATA_DIR, "preprocessed")
READY_DIR = os.path.join(DATA_DIR, "ready")

# 🗞 Allow import of everything for convenience
__all__ = [
    "FINAL_DIR",
    "MODEL_DIR",
    "UTILS_DIR",
    "SYSTEM_UTILS_DIR",
    "DATA_UTILS_DIR",
    "DATA_DIR",
    "ARTIFACTS_DIR",
    "SCRIPTS_DIR",
    "TESTS_DIR",
    "RAW_DIR",
    "FILTERED_DIR",
    "REFINED_DIR",
    "PREPROCESSED_DIR",
    "READY_DIR"
]
