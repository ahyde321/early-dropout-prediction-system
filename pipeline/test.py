import os
from preprocess_student_dropout_data import preprocess_student_dropout_data

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, '../data/raw/raw_dataset.csv')
train_file = os.path.join(script_dir, '../data/processed/preprocessed2.csv')
test_file = os.path.join(script_dir, '../data/test/test_preprocessed2.csv')


preprocess_student_dropout_data(input_file, train_file, test_file)