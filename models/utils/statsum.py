import pandas as pd
import sys
import os

# Set up base directory and file path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)
file_path = os.path.join(BASE_DIR, "data/results/enrolled_predictions.csv")

# Load the predictions file
df_preds = pd.read_csv(file_path)

# Display the first few rows
print("First 5 records:")
print(df_preds.head(), "\n")

# Show summary statistics (for numeric columns only)
print("Summary statistics for numeric columns:")
print(df_preds.describe(), "\n")

# Check the distribution of predictions
print("Distribution of 'Predicted Outcome':")
print(df_preds['Predicted Outcome'].value_counts(), "\n")

# Group-by analysis: Compute means and medians only for numeric columns
numeric_cols = df_preds.select_dtypes(include='number').columns.tolist()

group_means = df_preds.groupby('Predicted Outcome')[numeric_cols].mean()
group_medians = df_preds.groupby('Predicted Outcome')[numeric_cols].median()
print("Mean values by predicted outcome (numeric columns only):")
print(group_means, "\n")
print("Median values by predicted outcome (numeric columns only):")
print(group_medians, "\n")

# Compute a correlation matrix for numeric features only
print("Correlation matrix (numeric columns only):")
print(df_preds[numeric_cols].corr(), "\n")

# If the file contains a true label column, evaluate classification metrics.
if 'True Label' in df_preds.columns:
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

    y_true = df_preds['True Label']
    y_pred = df_preds['Predicted Outcome']
    
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    
    print("Classification Metrics:")
    print(f"Accuracy: {accuracy:.4f}\n")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(cm, "\n")
else:
    print("No true labels found for computing classification metrics.\n")

# Optional: Visualization code (uncomment if desired)
import matplotlib.pyplot as plt
df_preds['Age at enrollment'].hist(bins=20)
plt.title("Distribution of Age at Enrollment")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

df_preds['Predicted Outcome'].hist(bins=2)
plt.title("Distribution of Predicted Outcome")
plt.xlabel("Outcome (0=Dropout, 1=Graduate)")
plt.ylabel("Count")
plt.show()
