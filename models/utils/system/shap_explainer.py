import os
import pickle
import shap
import numpy as np
import logging
from typing import Optional
from models.utils.system.preprocessing import preprocess_row_for_inference
from models.feature_sets import FINAL_FIELDS, MID_FIELDS, EARLY_FIELDS

_model_cache = {}

def explain_student(student: dict, forced_phase: Optional[str] = None, base_model_dir: str = "models/"):
    """
    Generates SHAP feature attributions for a student's prediction.

    Args:
        student (dict): A dictionary of student features.
        forced_phase (str, optional): Force to use a specific phase ("early", "mid", "final").
        base_model_dir (str): Base path where model directories reside.

    Returns:
        dict: Mapping of feature names to SHAP values (float).
    """
    # === Determine Phase ===
    if forced_phase:
        phase = forced_phase
    else:
        if all(field in student and student[field] is not None for field in FINAL_FIELDS):
            phase = "final"
        elif all(field in student and student[field] is not None for field in MID_FIELDS):
            phase = "mid"
        elif all(field in student and student[field] is not None for field in EARLY_FIELDS):
            phase = "early"
        else:
            raise ValueError("Not enough data to generate SHAP explanation.")

    model_dir = os.path.join(base_model_dir, phase, "artifacts")
    model_path = os.path.join(model_dir, "random_forest_model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    # === Load and cache Model ===
    if phase in _model_cache:
        model = _model_cache[phase]
    else:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        _model_cache[phase] = model

    expected_features = list(model.feature_names_in_)

    # === Align Inputs ===
    raw_input = {k: student.get(k, 0) for k in expected_features}
    missing = [k for k in expected_features if k not in student or student[k] is None]
    if missing:
        logging.warning(f"[explain_student] Missing or null features for {phase} model: {missing}")

    # === Preprocess ===
    preprocessed_df = preprocess_row_for_inference(raw_input, model_dir, model=model)

    # === SHAP Calculation ===
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(preprocessed_df)

    # === Handle multi-output (binary classification)
    if isinstance(shap_values, list):
        shap_values = shap_values[0]  # Pick class 1 explanations (graduate)

    shap_array = shap_values[0]  # First row (student)

    feature_names = preprocessed_df.columns.tolist()

    shap_dict = {}
    for feature, value in zip(feature_names, shap_array):
        if isinstance(value, np.ndarray):
            if value.size == 2:
                # 🧠 pick Class 1 contribution ONLY
                value = value[1]
            elif value.size == 1:
                value = value.item()
            else:
                raise ValueError(f"Unexpected multi-value SHAP output for feature {feature}: {value}")
        shap_dict[feature] = float(value)

    print(f"[explain_student] ✅ Phase: {phase}, SHAP values generated.")

    return shap_dict
