import pandas as pd

# Load the predictions file
df_preds = pd.read_csv('/path/to/enrolled_predictions.csv')

# Display the first few rows
print(df_preds.head())

# Show summary statistics
print(df_preds.describe())

# Check the distribution of predictions
print(df_preds['Prediction'].value_counts())
