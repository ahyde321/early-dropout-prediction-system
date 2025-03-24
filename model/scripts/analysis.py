import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from utils.analysis_tools import *

predictions_file_path = os.path.join(BASE_DIR, "data/results/enrolled_predictions.csv")

df = load_data(predictions_file_path)
df = clean_data(df)

# Summarize and explore
print(summarize_data(df))
plot_grade_distribution(df)
correlation_matrix(df)

# Dropout analysis
dropout_factors = analyze_dropout_factors(df)
print("Factors most associated with dropouts:")
print(dropout_factors)

# Feature-wise dropout visualization
visualize_dropout_by_feature(df, 'Age at enrollment')
visualize_dropout_by_feature(df, 'Curricular units 1st sem (grade)')
visualize_dropout_by_feature(df, 'Curricular units 2nd sem (grade)')

# Define smaller grade bins for better visualization
grade_bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
grade_labels = ["0-2", "2-4", "4-6", "6-8", "8-10", "10-12", "12-14", "14-16", "16-18", "18-20"]
# Compute the average grade without modifying the dataset
df["Grade Category"] = pd.cut(df[["Curricular units 1st sem (grade)", "Curricular units 2nd sem (grade)"]].mean(axis=1),
                              bins=grade_bins, 
                              labels=grade_labels)

# Visualize dropout trends using the new binning
visualize_dropout_by_feature(df, "Grade Category")

visualize_dropout_by_feature(df, 'studied_credits')
