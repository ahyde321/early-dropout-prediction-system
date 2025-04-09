import os
import pickle
import logging
from models.utils.system.preprocessing import preprocess_row_for_inference
from models.feature_sets import FINAL_FIELDS, MID_FIELDS, EARLY_FIELDS

def predict_student(student: dict, base_model_dir: str = "models/", return_phase: bool = False):
    """
    Predicts graduation probability using the most complete available model phase.

    Args:
        student (dict): A dictionary of student features.
        base_model_dir (str): Base path where model directories reside.
        return_phase (bool): Whether to return the phase used in prediction.

    Returns:
        float or (float, str): Probability of graduation, optionally with the model phase.
    """
    # === Determine Phase ===
    if all(field in student and student[field] is not None for field in FINAL_FIELDS):
        phase = "final"
    elif all(field in student and student[field] is not None for field in MID_FIELDS):
        phase = "mid"
    elif all(field in student and student[field] is not None for field in EARLY_FIELDS):
        phase = "early"
    else:
        raise ValueError("Not enough data to make a prediction.")

    model_dir = os.path.join(base_model_dir, phase, "artifacts")

    # === Load Model ===
    model_path = os.path.join(model_dir, "random_forest_model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    expected_features = list(model.feature_names_in_)

    # === Align Inputs ===
    raw_input = {k: student.get(k, 0) for k in expected_features}
    missing = [k for k in expected_features if k not in student or student[k] is None]
    if missing:
        logging.warning(f"[predict_student] Missing or null features for {phase} model: {missing}")

    # === Preprocess ===
    preprocessed_df = preprocess_row_for_inference(raw_input, model_dir, model=model)

    # === Predict Graduation Probability ===
    prediction = float(model.predict_proba(preprocessed_df)[0][1])  # class 1 = Graduate
    print(f"[predict_student] Phase: {phase}, Graduation Probability: {prediction}")

    return (prediction, phase) if return_phase else prediction