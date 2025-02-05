import pandas as pd
import numpy as np
from sklearn.metrics import precision_recall_curve

def determine_optimal_threshold(probabilities, true_labels, plot=False):
    """
    Determine the optimal threshold based on the precision-recall curve.

    Args:
        probabilities (list or array): Predicted probabilities for the positive class.
        true_labels (list or array): True labels (must be numeric: 0 or 1).
        plot (bool): Whether to plot the precision-recall curve.

    Returns:
        float: The optimal threshold.
    """
    import pandas as pd
    import numpy as np
    from sklearn.metrics import precision_recall_curve
    import matplotlib.pyplot as plt

    try:
        # Convert labels to numeric if necessary and check validity
        true_labels = pd.Series(true_labels).astype(int)
        unique_labels = true_labels.unique()

        print(f"Unique labels in true_labels: {unique_labels}")

        if not set(unique_labels).issubset({0, 1}):
            raise ValueError(f"Invalid labels found: {unique_labels}. Labels must be binary (0 and 1).")

    except Exception as e:
        print(f"Error during label conversion: {e}")
        raise

    # Calculate precision-recall curve
    precision, recall, thresholds = precision_recall_curve(true_labels, probabilities)

    if plot:
        plt.plot(thresholds, precision[:-1], label='Precision')
        plt.plot(thresholds, recall[:-1], label='Recall')
        plt.xlabel('Threshold')
        plt.ylabel('Score')
        plt.title('Precision-Recall Curve')
        plt.legend()
        plt.grid(True)
        plt.show()

    # Find the optimal threshold where precision and recall are balanced
    optimal_index = np.argmin(np.abs(precision - recall))
    return thresholds[optimal_index] if len(thresholds) > 0 else 0.5  # Default to 0.5 if no thresholds found


def classify_predictions(probabilities, threshold=0.6):
    """Classify predictions based on the given threshold."""
    # Check if probabilities array is empty
    if len(probabilities) == 0:
        return []
    
    return ["High Risk (Dropout)" if prob > threshold else "Likely Graduate" for prob in probabilities]


