import os
import pickle
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# These match the fields used in prediction phase selection
from models.utils.system.prediction import EARLY_FIELDS, MID_FIELDS, FINAL_FIELDS

# === Constants ===
PHASES = ["early", "mid", "final"]
ARTIFACT_NAME = "random_forest_model.pkl"
TEST_DATA_NAME = "test_data.pkl"

def get_model_path(phase: str, base_model_dir: str = "models/"):
    return os.path.join(base_model_dir, phase, "artifacts", ARTIFACT_NAME)

def get_test_data_path(phase: str, base_model_dir: str = "models/"):
    return os.path.join(base_model_dir, phase, "artifacts", TEST_DATA_NAME)

def load_model(phase: str, base_model_dir: str = "models/"):
    path = get_model_path(phase, base_model_dir)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found at {path}")
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model

def get_feature_importance(model):
    if hasattr(model, "feature_importances_"):
        return dict(zip(model.feature_names_in_, model.feature_importances_))
    elif hasattr(model, "coef_"):
        return dict(zip(model.feature_names_in_, model.coef_[0]))
    return {}

def get_model_metrics(phase: str, base_model_dir: str = "models/"):
    test_path = get_test_data_path(phase, base_model_dir)
    if not os.path.exists(test_path):
        return {"warning": "No test data found for this phase"}

    X_test, y_test = joblib.load(test_path)
    model = load_model(phase, base_model_dir)
    y_pred = model.predict(X_test)

    return {
        "accuracy": round(accuracy_score(y_test, y_pred), 3),
        "precision": round(precision_score(y_test, y_pred, average="macro"), 3),
        "recall": round(recall_score(y_test, y_pred, average="macro"), 3),
        "f1_score": round(f1_score(y_test, y_pred, average="macro"), 3)
    }

def get_model_info(phase: str = None, base_model_dir: str = "models/"):
    phases = [phase] if phase else PHASES
    results = {}

    for p in phases:
        try:
            model = load_model(p, base_model_dir)
            results[p] = {
                "metrics": get_model_metrics(p, base_model_dir),
                "feature_importance": get_feature_importance(model)
            }
        except FileNotFoundError as e:
            results[p] = {"error": str(e)}

    return results
