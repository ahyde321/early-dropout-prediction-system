import os
from validate_model import validate_dropout_model

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

print("Starting the validation process...")
validate_dropout_model(base_dir)
print("Validation completed successfully.")
