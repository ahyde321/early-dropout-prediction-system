import os
import pickle
import logging

from models.feature_sets import EARLY_FIELDS, MID_FIELDS, FINAL_FIELDS
from .preprocessing import preprocess_row_for_inference

def predict_student(student: dict, base_model_dir: str = "models/") -> float:
    if all(field in student and student[field] is not None for field in FINAL_FIELDS):
        phase = "final"
    elif all(field in student and student[field] is not None for field in MID_FIELDS):
        phase = "mid"
    elif all(field in student and student[field] is not None for field in EARLY_FIELDS):
        phase = "early"
    else:
        raise ValueError("Not enough data to make a prediction.")

    print(f"Using {phase.upper()} model for prediction")

    model_dir = os.path.join(base_model_dir, phase, "artifacts")

    # Load model
    with open(os.path.join(model_dir, "random_forest_model.pkl"), "rb") as f:
        model = pickle.load(f)

    # ✅ Use model's own feature list
    expected_features = list(model.feature_names_in_)
    raw_input = {k: student.get(k, 0) for k in expected_features}

    print("🧪 Raw input keys:", list(raw_input.keys()))
    print("🧪 Raw input values:", raw_input)

    # Preprocess
    preprocessed_df = preprocess_row_for_inference(raw_input, model_dir, model=model)

    print("✅ Preprocessed columns:", list(preprocessed_df.columns))
    print("✅ Model expects:", list(model.feature_names_in_))

    return float(model.predict_proba(preprocessed_df)[0][1])
