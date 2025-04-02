import pandas as pd
import re
import uuid

# Step 1: Convert headers to snake_case
def to_snake_case_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [re.sub(r'\W+', '_', col).strip().lower() for col in df.columns]
    return df

# Step 2: Assign first/last name and student number (if not present)
def enrich_students(df: pd.DataFrame) -> pd.DataFrame:
    if 'first_name' not in df.columns:
        df['first_name'] = generate_fake_names(df.shape[0], kind='first')
    if 'last_name' not in df.columns:
        df['last_name'] = generate_fake_names(df.shape[0], kind='last')
    if 'student_number' not in df.columns:
        df['student_number'] = [str(uuid.uuid4())[:8] for _ in range(df.shape[0])]
    return df

# Utility: Generate dummy names (replace with faker if needed)
def generate_fake_names(n, kind='first'):
    first = ['Alice', 'Bob', 'Charlie', 'Dana', 'Eli']
    last = ['Smith', 'Jones', 'Taylor', 'Brown', 'Patel']
    return [first[i % len(first)] if kind == 'first' else last[i % len(last)] for i in range(n)]

# Master pipeline function
def process_student_upload(df: pd.DataFrame) -> pd.DataFrame:
    df = to_snake_case_columns(df)
    df = enrich_students(df)
    return df
