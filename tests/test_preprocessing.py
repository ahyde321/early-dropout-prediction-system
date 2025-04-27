import unittest
from unittest.mock import patch, MagicMock, mock_open
import numpy as np
import pandas as pd
import os
import pickle

from models.utils.system.preprocessing import preprocess_row_for_inference

class TestPreprocessing(unittest.TestCase):
    """Tests for the preprocessing.py module"""
    
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_preprocess_row_for_inference_basic(self, mock_file_open, mock_pickle_load):
        """Test basic functionality of preprocess_row_for_inference"""
        # Setup mock model
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['age', 'gender', 'course_grade']
        
        # Setup mock encoders and scaler
        mock_encoders = {'gender': MagicMock()}
        mock_encoders['gender'].transform.return_value = np.array([1])
        mock_encoders['gender'].classes_ = ['M', 'F']
        
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([[0.5, 0.8]])
        
        # Configure pickle.load to return different objects on consecutive calls
        mock_pickle_load.side_effect = [mock_encoders, mock_scaler]
        
        # Input data
        data = {
            'age': 20,
            'gender': 'F',
            'course_grade': 85,
            'extra_field': 'not_used'  # Should be dropped
        }
        
        # Call the function
        result = preprocess_row_for_inference(data, 'mock_model_dir', mock_model)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ['age', 'gender', 'course_grade'])
        self.assertEqual(result.shape, (1, 3))
        
        # Check if extra field was dropped
        self.assertNotIn('extra_field', result.columns)
        
        # Verify the open calls were made correctly
        mock_file_open.assert_any_call(os.path.join('mock_model_dir', 'label_encoders.pkl'), 'rb')
        mock_file_open.assert_any_call(os.path.join('mock_model_dir', 'scaler.pkl'), 'rb')
        
        # Verify label encoder was used for categorical column
        mock_encoders['gender'].transform.assert_called_once_with(['F'])
        
        # Verify scaler was applied to numerical columns
        mock_scaler.transform.assert_called_once()
    
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_preprocess_row_missing_columns(self, mock_file_open, mock_pickle_load):
        """Test preprocessing with missing columns"""
        # Setup mock model
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['age', 'gender', 'course_grade', 'missing_col']
        
        # Setup mock encoders and scaler
        mock_encoders = {'gender': MagicMock()}
        mock_encoders['gender'].transform.return_value = np.array([1])
        mock_encoders['gender'].classes_ = ['M', 'F']
        
        mock_scaler = MagicMock()
        # Return scaled values for age, course_grade, and missing_col
        mock_scaler.transform.return_value = np.array([[0.5, 0.8, 0.0]])
        
        # Configure pickle.load
        mock_pickle_load.side_effect = [mock_encoders, mock_scaler]
        
        # Input data (missing 'missing_col')
        data = {
            'age': 20,
            'gender': 'F',
            'course_grade': 85
        }
        
        # Call the function
        result = preprocess_row_for_inference(data, 'mock_model_dir', mock_model)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ['age', 'gender', 'course_grade', 'missing_col'])
        self.assertEqual(result.shape, (1, 4))
        
        # Check that missing column was added with default value 0
        self.assertEqual(result['missing_col'].iloc[0], 0)
    
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_preprocess_row_unknown_categorical_value(self, mock_file_open, mock_pickle_load):
        """Test preprocessing with unknown categorical value"""
        # Setup mock model
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['age', 'gender', 'course_grade']
        
        # Setup mock encoders and scaler
        mock_encoders = {'gender': MagicMock()}
        # Simulate encoder behavior when an unknown value is provided
        mock_encoders['gender'].transform.side_effect = KeyError("'Unknown' is not in list")
        mock_encoders['gender'].classes_ = ['M', 'F']
        
        mock_scaler = MagicMock()
        # Fix: Return array with correct number of columns for age and course_grade
        mock_scaler.transform.return_value = np.array([[0.5, 0.8]])
        
        # Configure pickle.load
        mock_pickle_load.side_effect = [mock_encoders, mock_scaler]
        
        # Input data with unknown gender
        data = {
            'age': 20,
            'gender': 'Unknown',  # Not in encoder classes
            'course_grade': 85
        }
        
        # Call the function
        result = preprocess_row_for_inference(data, 'mock_model_dir', mock_model)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        
        # Apply function should handle this by returning -1
        # Mocking the apply function's behavior
        self.assertEqual(result['gender'].iloc[0], -1)
    
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_preprocess_row_no_categorical_columns(self, mock_file_open, mock_pickle_load):
        """Test preprocessing with only numerical columns"""
        # Setup mock model
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['age', 'course_grade', 'study_hours']
        
        # Setup mock encoders and scaler
        mock_encoders = {}  # No encoders needed
        
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([[0.5, 0.8, 0.3]])
        
        # Configure pickle.load
        mock_pickle_load.side_effect = [mock_encoders, mock_scaler]
        
        # Input data - all numerical
        data = {
            'age': 20,
            'course_grade': 85,
            'study_hours': 40
        }
        
        # Call the function
        result = preprocess_row_for_inference(data, 'mock_model_dir', mock_model)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ['age', 'course_grade', 'study_hours'])
        
        # Verify scaler was applied to all columns
        mock_scaler.transform.assert_called_once()
    
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_preprocess_row_no_numerical_columns(self, mock_file_open, mock_pickle_load):
        """Test preprocessing with only categorical columns"""
        # Setup mock model
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['gender', 'marital_status', 'enrollment_type']
        
        # Setup mock encoders and scaler
        mock_encoders = {
            'gender': MagicMock(),
            'marital_status': MagicMock(),
            'enrollment_type': MagicMock()
        }
        mock_encoders['gender'].transform.return_value = np.array([1])
        mock_encoders['gender'].classes_ = ['M', 'F']
        mock_encoders['marital_status'].transform.return_value = np.array([0])
        mock_encoders['marital_status'].classes_ = ['Single', 'Married']
        mock_encoders['enrollment_type'].transform.return_value = np.array([1])
        mock_encoders['enrollment_type'].classes_ = ['Full-time', 'Part-time']
        
        mock_scaler = MagicMock()
        
        # Configure pickle.load
        mock_pickle_load.side_effect = [mock_encoders, mock_scaler]
        
        # Input data - all categorical
        data = {
            'gender': 'F',
            'marital_status': 'Single',
            'enrollment_type': 'Part-time'
        }
        
        # Call the function
        result = preprocess_row_for_inference(data, 'mock_model_dir', mock_model)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ['gender', 'marital_status', 'enrollment_type'])
        
        # Verify label encoders were used
        mock_encoders['gender'].transform.assert_called_once()
        mock_encoders['marital_status'].transform.assert_called_once()
        mock_encoders['enrollment_type'].transform.assert_called_once()
        
        # Verify scaler was not applied (num_cols is empty)
        mock_scaler.transform.assert_not_called()
    
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_preprocess_row_drop_unwanted_columns(self, mock_file_open, mock_pickle_load):
        """Test preprocessing with columns that should be dropped"""
        # Setup mock model
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['age', 'gender']
        
        # Setup mock encoders and scaler
        mock_encoders = {'gender': MagicMock()}
        mock_encoders['gender'].transform.return_value = np.array([1])
        mock_encoders['gender'].classes_ = ['M', 'F']
        
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([[0.5]])
        
        # Configure pickle.load
        mock_pickle_load.side_effect = [mock_encoders, mock_scaler]
        
        # Input data with target and original_index that should be dropped
        data = {
            'age': 20,
            'gender': 'F',
            'target': 1,  # Should be dropped
            'original_index': 42  # Should be dropped
        }
        
        # Call the function
        result = preprocess_row_for_inference(data, 'mock_model_dir', mock_model)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ['age', 'gender'])
        
        # Check that target and original_index were dropped
        self.assertNotIn('target', result.columns)
        self.assertNotIn('original_index', result.columns)

if __name__ == '__main__':
    unittest.main() 