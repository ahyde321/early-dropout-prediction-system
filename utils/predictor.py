import os
import pandas as pd
import pickle

def load_model(model_path):
    """Load the trained model from file."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def predict_new_data(model_path, data_path, output_path):
    """Make predictions on new enrolled students."""
    model = load_model(model_path)
    X_enrolled = pd.read_csv(data_path)

    predictions = model.predict(X_enrolled)
    output_df = pd.DataFrame(predictions, columns=["Predicted Target"])
    output_df.to_csv(output_path, index=False)

    print(f"📂 Predictions saved at: {output_path}")
