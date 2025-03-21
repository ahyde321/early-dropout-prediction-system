import pandas as pd

# Load the dataset
file_path = "data/filtered/past.csv"  # Change this if using another dataset
df = pd.read_csv(file_path)

# Count the number of students in each target category (Dropout, Graduate, etc.)
target_counts = df['Target'].value_counts()
total_students = len(df)

# Display the results
print("Number of students per category:")
print(target_counts)
print(f"\nTotal number of students: {total_students}")
