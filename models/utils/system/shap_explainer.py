import shap
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional

def explain_global(model, X_val: pd.DataFrame, output_path: Optional[str] = None):
    """
    Generates a SHAP beeswarm plot for the positive class in a binary classifier.

    Args:
        model: Trained tree-based classifier.
        X_val (pd.DataFrame): Input features (same as used in prediction).
        output_path (str, optional): If given, saves the plot as a PNG.
    """
    explainer = shap.Explainer(model, X_val)
    shap_values = explainer(X_val)

    if shap_values.values.ndim == 3:  # (samples, features, classes)
        shap_values = shap.Explanation(
            values=shap_values.values[:, :, 1],              # class 1
            base_values=shap_values.base_values[:, 1],
            data=shap_values.data,
            feature_names=shap_values.feature_names
        )

    assert shap_values.values.shape == X_val.shape, "Mismatch between SHAP values and input features."

    shap.plots.beeswarm(shap_values, show=False)

    if output_path:
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()
        print(f"📊 SHAP summary plot saved to: {output_path}")
    else:
        plt.show()


def explain_student(model, X_val: pd.DataFrame, index: int = 0):
    """
    Returns a SHAP force plot for a single student's prediction explanation.

    Args:
        model: Trained tree-based model.
        X_val (pd.DataFrame): Validation features.
        index (int): Row index of the student to explain.

    Returns:
        SHAP HTML force plot object (interactive).
    """
    if index < 0 or index >= len(X_val):
        raise IndexError(f"Index {index} is out of bounds for X_val with {len(X_val)} rows.")

    explainer = shap.Explainer(model, X_val)
    shap_values = explainer(X_val)

    if shap_values.values.ndim == 3:
        shap_values = shap.Explanation(
            values=shap_values.values[:, :, 1],
            base_values=shap_values.base_values[:, 1],
            data=shap_values.data,
            feature_names=shap_values.feature_names
        )

    return shap.plots.force(
        shap_values[index].base_values,
        shap_values[index].values,
        X_val.iloc[index]
    )
