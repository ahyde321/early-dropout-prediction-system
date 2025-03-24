import os
import sys

# 📁 Absolute path to the "early" directory
EARLY_DIR = os.path.dirname(os.path.abspath(__file__))

# 📁 Go up one level to get to "models"
MODEL_DIR = os.path.dirname(EARLY_DIR)

# 📁 Path to the shared "utils" directory
UTILS_DIR = os.path.join(MODEL_DIR, "utils")

# ➕ Add utils directory to sys.path so imports work
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# 📂 Define key directories used across early model scripts/tests
DATA_DIR = os.path.join(EARLY_DIR, "data")
ARTIFACTS_DIR = os.path.join(EARLY_DIR, "artifacts")
SCRIPTS_DIR = os.path.join(EARLY_DIR, "scripts")
TESTS_DIR = os.path.join(EARLY_DIR, "tests")

# 📂 Subdirectories for data pipeline
# 📁 Raw data (shared between early/final)
RAW_DIR = os.path.join(MODEL_DIR, "data", "raw")
FILTERED_DIR = os.path.join(DATA_DIR, "filtered")
REFINED_DIR = os.path.join(DATA_DIR, "refined")
PREPROCESSED_DIR = os.path.join(DATA_DIR, "preprocessed")
READY_DIR = os.path.join(DATA_DIR, "ready")

# 🧾 Allow import of everything for convenience
__all__ = [
    "EARLY_DIR",
    "MODEL_DIR",
    "UTILS_DIR",
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
