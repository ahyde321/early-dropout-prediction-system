import pandas as pd

# Load datasets
df1 = pd.read_csv("data/raw/raw_dataset1.csv")
df2 = pd.read_csv("data/raw/raw_dataset2.csv")

# Get unique values and counts
print("\n📊 Dataset 1 - Application Mode Counts:")
print(df1["Application mode"].value_counts())

print("\n📊 Dataset 2 - Application Mode Counts:")
print(df2["Application mode"].value_counts())
