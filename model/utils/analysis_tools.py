import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    """Loads the dataset from a CSV file."""
    return pd.read_csv(filepath)

def clean_data(df):
    """Cleans the dataset by handling missing values and converting data types."""
    df = df.dropna()  # You can replace this with imputation if needed
    return df

def summarize_data(df):
    """Returns basic statistics of numeric columns."""
    return df.describe()

def plot_grade_distribution(df, column='Predicted Label'):
    """Plots the distribution of student grades or results."""
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x=column)
    plt.title("Distribution of Final Results")
    plt.xlabel("Final Result")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.show()

def correlation_matrix(df):
    """Plots a heatmap of correlation between numerical features."""
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.show()

def analyze_dropout_factors(df, result_col='Predicted Label', target='Dropout'):
    """Analyzes what features are most correlated with dropouts."""
    df['is_dropout'] = df[result_col] == target
    dropout_rates = df.groupby('is_dropout').mean(numeric_only=True).T
    return dropout_rates.sort_values(by=True, ascending=False)

def visualize_dropout_by_feature(df, feature, result_col='Predicted Label'):
    """Visualizes dropout trends by a specific feature."""
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x=feature, hue=result_col)
    plt.title(f"Dropout Trends by {feature}")
    plt.tight_layout()
    plt.show()
