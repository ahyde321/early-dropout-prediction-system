import os
import sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

from pipeline.preprocess_student_dropout_data import preprocess_student_dropout_data

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, '../data/raw/combined_raw_dataset.csv')
output_dir = os.path.join(script_dir, '../data/processed/')
preprocessed_enrolled = os.path.join(script_dir, '../data/enrolled/preprocessed_enrolled.csv')
raw_enrolled = os.path.join(script_dir, '../data/enrolled/raw_enrolled.csv')

preprocess_student_dropout_data(input_file, output_dir, preprocessed_enrolled, raw_enrolled)