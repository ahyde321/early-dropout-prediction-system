import os
import pickle
from models.feature_sets import EARLY_FIELDS, MID_FIELDS, FINAL_FIELDS
from .preprocessing import preprocess_row_for_inference  # adjust import if needed
from ..data.data_preprocessor import preprocess_row_for_inference 

def predict_student(student: dict, base_model_dir: str = "models/") -> float:
    if all(field in student and student[field] is not None for field in FINAL_FIELDS):
        phase = "final"
        features = FINAL_FIELDS
    elif all(field in student and student[field] is not None for field in MID_FIELDS):
        phase = "mid"
        features = MID_FIELDS
    elif all(field in student and student[field] is not None for field in EARLY_FIELDS):
        phase = "early"
        features = EARLY_FIELDS
    else:
        raise ValueError("Not enough data to make a prediction.")

    model_dir = os.path.join(base_model_dir, phase, "artifacts")

    # Load model
    with open(os.path.join(model_dir, "random_forest_model.pkl"), "rb") as f:
        model = pickle.load(f)

    # Slice input
    raw_input = {k: student[k] for k in features if k in student}
    preprocessed_df = preprocess_row_for_inference(raw_input, model_dir)

    return float(model.predict_proba(preprocessed_df)[0][1])
