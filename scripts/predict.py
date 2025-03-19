import os
from utils.predictor import predict_new_data

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models/random_forest_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data/preprocessed/preprocessed_enrolled_pupils.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data/results/enrolled_predictions.csv")

# Run predictions
predict_new_data(
    model_path=MODEL_PATH,
    data_path=DATA_PATH,
    output_path=OUTPUT_PATH
)
