import os
import sys

# Absolute path to the "models" directory
MODELS_DIR = os.path.dirname(os.path.abspath(__file__))

# 📁 Paths to submodules
DATA_DIR = os.path.join(MODELS_DIR, "data")
ENROLLED_DIR = os.path.join(DATA_DIR, "enrolled")
RAW_DIR = os.path.join(DATA_DIR, "raw")
FILTERED_DIR = os.path.join(DATA_DIR, "filtered")   
REFINED_DIR = os.path.join(DATA_DIR, "refined")      
PREPROCESSED_DIR = os.path.join(DATA_DIR, "preprocessed") 
READY_DIR = os.path.join(DATA_DIR, "ready")        
ARTIFACTS_DIR = os.path.join(MODELS_DIR, "artifacts")

EARLY_DIR = os.path.join(MODELS_DIR, "early")
EARLY_DATA_DIR = os.path.join(EARLY_DIR, "data")
EARLY_ARTIFACTS_DIR = os.path.join(EARLY_DIR, "artifacts")
EARLY_SCRIPTS_DIR = os.path.join(EARLY_DIR, "scripts")
EARLY_TESTS_DIR = os.path.join(EARLY_DIR, "tests")

FINAL_DIR = os.path.join(MODELS_DIR, "final")
MID_DIR = os.path.join(MODELS_DIR, "mid")

UTILS_DIR = os.path.join(MODELS_DIR, "utils")
SCRIPTS_DIR = os.path.join(MODELS_DIR, "scripts")

# ➕ Add utils directory to sys.path so imports work
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

#  Allow import of everything for convenience
__all__ = [
    "MODELS_DIR",
    "DATA_DIR", "ENROLLED_DIR", "RAW_DIR",
    "FILTERED_DIR", "REFINED_DIR", "PREPROCESSED_DIR", "READY_DIR",
    "EARLY_DIR", "EARLY_DATA_DIR", "EARLY_ARTIFACTS_DIR", "EARLY_SCRIPTS_DIR", "EARLY_TESTS_DIR",
    "FINAL_DIR", "MID_DIR",
    "ARTIFACTS_DIR",
    "UTILS_DIR", "SCRIPTS_DIR"
]
