import os
import pandas as pd
import pickle

def load_model(model_path):
    """Load the trained model from file."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def predict_new_data(model_path, data_path, output_path):
    """
    Make predictions on any dataset using a trained model.

    Parameters:
    - model_path (str): Path to the trained model file.
    - data_path (str): Path to the dataset (features only, preprocessed).
    - output_path (str): Path to save predictions.

    Returns:
    - pd.DataFrame: The dataset with predictions included.
    """

    # ✅ Load trained model
    model = load_model(model_path)

    # ✅ Load dataset to predict on
    X_new = pd.read_csv(data_path)

    # ✅ Make predictions
    predictions = model.predict(X_new)

    # ✅ Create a DataFrame for predictions
    predictions_df = pd.DataFrame(predictions, columns=["Predicted Outcome"])

    # ✅ Save predictions
    predictions_df.to_csv(output_path, index=False)

    print(f"✅ Predictions saved at: {output_path}")
    return predictions_df
