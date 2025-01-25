import os
import sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

from pipeline.preprocess_student_dropout_data import preprocess_student_dropout_data

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, '../data/raw/raw_dataset1.csv')
train_file = os.path.join(script_dir, '../data/processed/preprocessed1.csv')
test_file = os.path.join(script_dir, '../data/test/enrolled1.csv')
raw_test = os.path.join(script_dir, '../data/test/raw_enrolled1.csv')



preprocess_student_dropout_data(input_file, train_file, test_file, raw_test)