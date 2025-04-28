import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import numpy as np
import pandas as pd
import shap
import os
import pytest

from models.utils.system.shap_explainer import explain_student

class TestShapExplainer(unittest.TestCase):
    """Tests for the SHAP explainer module"""
    
    @pytest.mark.skip(reason="Replaced by test_explain_student_final_phase_impl")
    @patch('os.path.exists')
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('models.utils.system.shap_explainer.preprocess_row_for_inference')
    @patch('shap.TreeExplainer')
    @patch('models.utils.system.shap_explainer.FINAL_FIELDS', ['student_number', 'first_name', 'last_name', 'marital_status', 'previous_qualification_grade', 'admission_grade', 'displaced', 'debtor', 'tuition_fees_up_to_date', 'gender', 'scholarship_holder', 'age_at_enrollment', 'curricular_units_1st_sem_enrolled', 'curricular_units_1st_sem_approved', 'curricular_units_1st_sem_grade', 'curricular_units_2nd_sem_grade'])
    @patch('models.utils.system.shap_explainer.MID_FIELDS', ['student_number', 'curricular_units_1st_sem_approved', 'curricular_units_1st_sem_grade'])
    @patch('models.utils.system.shap_explainer.EARLY_FIELDS', ['student_number', 'first_name', 'last_name', 'marital_status', 'previous_qualification_grade', 'admission_grade', 'displaced', 'debtor', 'tuition_fees_up_to_date', 'gender', 'scholarship_holder', 'age_at_enrollment', 'curricular_units_1st_sem_enrolled'])
    def test_explain_student_final_phase(self):
        """Test explaining a student in the final phase"""
        self.test_explain_student_final_phase_impl()
    
    def test_explain_student_final_phase_impl(self):
        """Implementation of the test for final phase data using context managers"""
        # Create student data with all required fields for final phase
        student_data = {
            'student_number': '12345',
            'first_name': 'Test',
            'last_name': 'Student',
            'marital_status': 1,
            'previous_qualification_grade': 14.0,
            'admission_grade': 140.0,
            'displaced': 1,
            'debtor': 0,
            'tuition_fees_up_to_date': 1,
            'gender': 0,
            'scholarship_holder': 0,
            'age_at_enrollment': 18,
            'curricular_units_1st_sem_enrolled': 6,
            'curricular_units_1st_sem_approved': 5,
            'curricular_units_1st_sem_grade': 14.5,
            'curricular_units_2nd_sem_grade': 15.0
        }
        
        # Use context managers for patching
        with patch('models.utils.system.shap_explainer.EARLY_FIELDS', 
                  ['student_number', 'first_name', 'last_name', 'marital_status', 
                   'previous_qualification_grade', 'admission_grade', 'displaced', 
                   'debtor', 'tuition_fees_up_to_date', 'gender', 'scholarship_holder', 
                   'age_at_enrollment', 'curricular_units_1st_sem_enrolled']), \
             patch('models.utils.system.shap_explainer.MID_FIELDS', 
                  ['student_number', 'curricular_units_1st_sem_approved', 
                   'curricular_units_1st_sem_grade']), \
             patch('models.utils.system.shap_explainer.FINAL_FIELDS', 
                  ['student_number', 'curricular_units_1st_sem_approved', 
                   'curricular_units_1st_sem_grade', 'curricular_units_2nd_sem_grade']), \
             patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open()) as mock_file_open, \
             patch('pickle.load') as mock_pickle_load, \
             patch('models.utils.system.shap_explainer.preprocess_row_for_inference') as mock_preprocess, \
             patch('shap.TreeExplainer') as mock_tree_explainer:
                
            # Mock model
            mock_model = MagicMock()
            mock_model.feature_names_in_ = ['feature1', 'feature2']
            mock_pickle_load.return_value = mock_model
            
            # Mock preprocessed data
            mock_df = pd.DataFrame({
                'feature1': [0.5],
                'feature2': [0.7]
            })
            mock_preprocess.return_value = mock_df
            
            # Mock SHAP explainer
            mock_explainer = MagicMock()
            mock_tree_explainer.return_value = mock_explainer
            
            # Mock SHAP values
            mock_shap_values = np.array([[0.2, 0.3]])
            mock_explainer.shap_values.return_value = mock_shap_values
            
            # Call the function
            result = explain_student(student_data)
            
            # Assertions
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 2)
            self.assertEqual(result['feature1'], 0.2)
            self.assertEqual(result['feature2'], 0.3)
            
            # Verify model loading with correct phase
            mock_file_open.assert_called_with('models/final/artifacts/random_forest_model.pkl', 'rb')
    
    def test_explain_student_mid_phase(self):
        """Test explain_student function with mid phase data"""
        # Create student data with mid phase fields but without final fields
        student_data = {
            'student_number': '12345',
            'first_name': 'Test',
            'last_name': 'Student',
            'marital_status': 1,
            'previous_qualification_grade': 14.0,
            'admission_grade': 140.0,
            'displaced': 1,
            'debtor': 0,
            'tuition_fees_up_to_date': 1,
            'gender': 0,
            'scholarship_holder': 0,
            'age_at_enrollment': 18,
            'curricular_units_1st_sem_enrolled': 6,
            'curricular_units_1st_sem_approved': 5,
            'curricular_units_1st_sem_grade': 14.5,
            # No 2nd semester grade
        }
        
        # Use context managers for patching instead of decorators
        with patch('models.utils.system.shap_explainer.EARLY_FIELDS', 
                  ['student_number', 'first_name', 'last_name', 'marital_status', 
                   'previous_qualification_grade', 'admission_grade', 'displaced', 
                   'debtor', 'tuition_fees_up_to_date', 'gender', 'scholarship_holder', 
                   'age_at_enrollment', 'curricular_units_1st_sem_enrolled']), \
             patch('models.utils.system.shap_explainer.MID_FIELDS', 
                  ['student_number', 'curricular_units_1st_sem_approved', 
                   'curricular_units_1st_sem_grade']), \
             patch('models.utils.system.shap_explainer.FINAL_FIELDS', 
                  ['student_number', 'curricular_units_1st_sem_approved', 
                   'curricular_units_1st_sem_grade', 'curricular_units_2nd_sem_grade']), \
             patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open()) as mock_file_open, \
             patch('pickle.load') as mock_pickle_load, \
             patch('models.utils.system.shap_explainer.preprocess_row_for_inference') as mock_preprocess, \
             patch('shap.TreeExplainer') as mock_tree_explainer:
                
            # Mock model
            mock_model = MagicMock()
            mock_model.feature_names_in_ = ['feature1', 'feature2']
            mock_pickle_load.return_value = mock_model
            
            # Mock preprocessed data
            mock_df = pd.DataFrame({
                'feature1': [0.5],
                'feature2': [0.7]
            })
            mock_preprocess.return_value = mock_df
            
            # Mock SHAP explainer
            mock_explainer = MagicMock()
            mock_tree_explainer.return_value = mock_explainer
            
            # Mock SHAP values
            mock_shap_values = np.array([[0.2, 0.3]])
            mock_explainer.shap_values.return_value = mock_shap_values
            
            # Call the function
            result = explain_student(student_data)
            
            # Assertions
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 2)
            self.assertEqual(result['feature1'], 0.2)
            self.assertEqual(result['feature2'], 0.3)
            
            # Verify model loading with correct phase
            mock_file_open.assert_called_with('models/mid/artifacts/random_forest_model.pkl', 'rb')
    
    def test_explain_student_early_phase(self):
        """Test explain_student function with early phase data"""
        # Create student data with only early phase fields
        student_data = {
            'student_number': '12345',
            'first_name': 'Test',
            'last_name': 'Student',
            'marital_status': 1,
            'previous_qualification_grade': 14.0,
            'admission_grade': 140.0,
            'displaced': 1,
            'debtor': 0,
            'tuition_fees_up_to_date': 1,
            'gender': 0,
            'scholarship_holder': 0,
            'age_at_enrollment': 18,
            'curricular_units_1st_sem_enrolled': 6,
            # No semester grades or approvals
        }
        
        # Use context managers for patching instead of decorators
        with patch('models.utils.system.shap_explainer.EARLY_FIELDS', 
                  ['student_number', 'first_name', 'last_name', 'marital_status', 
                   'previous_qualification_grade', 'admission_grade', 'displaced', 
                   'debtor', 'tuition_fees_up_to_date', 'gender', 'scholarship_holder', 
                   'age_at_enrollment', 'curricular_units_1st_sem_enrolled']), \
             patch('models.utils.system.shap_explainer.MID_FIELDS', 
                  ['student_number', 'curricular_units_1st_sem_approved', 
                   'curricular_units_1st_sem_grade']), \
             patch('models.utils.system.shap_explainer.FINAL_FIELDS', 
                  ['student_number', 'curricular_units_1st_sem_approved', 
                   'curricular_units_1st_sem_grade', 'curricular_units_2nd_sem_grade']), \
             patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open()) as mock_file_open, \
             patch('pickle.load') as mock_pickle_load, \
             patch('models.utils.system.shap_explainer.preprocess_row_for_inference') as mock_preprocess, \
             patch('shap.TreeExplainer') as mock_tree_explainer:
                
            # Mock model
            mock_model = MagicMock()
            mock_model.feature_names_in_ = ['feature1', 'feature2']
            mock_pickle_load.return_value = mock_model
            
            # Mock preprocessed data
            mock_df = pd.DataFrame({
                'feature1': [0.5],
                'feature2': [0.7]
            })
            mock_preprocess.return_value = mock_df
            
            # Mock SHAP explainer
            mock_explainer = MagicMock()
            mock_tree_explainer.return_value = mock_explainer
            
            # Mock SHAP values
            mock_shap_values = np.array([[0.2, 0.3]])
            mock_explainer.shap_values.return_value = mock_shap_values
            
            # Call the function
            result = explain_student(student_data)
            
            # Assertions
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 2)
            self.assertEqual(result['feature1'], 0.2)
            self.assertEqual(result['feature2'], 0.3)
            
            # Verify model loading with correct phase
            mock_file_open.assert_called_with('models/early/artifacts/random_forest_model.pkl', 'rb')
    
    def test_explain_student_forced_phase(self):
        """Test explain_student function with forced phase parameter"""
        # Create student data with minimal fields
        student_data = {
            'student_number': '12345',
            'gender': 0,
            'age_at_enrollment': 18,
        }
        
        # Use multiple patches to fully control the execution
        mock_open_instance = mock_open()
        with patch('models.utils.system.shap_explainer.EARLY_FIELDS', ['student_number']), \
             patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open_instance), \
             patch('pickle.load') as mock_load, \
             patch('models.utils.system.shap_explainer.preprocess_row_for_inference') as mock_preprocess, \
             patch('models.utils.system.shap_explainer._model_cache', {}), \
             patch('shap.TreeExplainer') as mock_explainer:
            
            # Set up mock returns
            mock_model = MagicMock()
            mock_load.return_value = mock_model
            
            mock_preprocess.return_value = pd.DataFrame({
                'feature1': [0.5],
                'feature2': [0.7]
            })
            
            explainer_instance = MagicMock()
            mock_explainer.return_value = explainer_instance
            explainer_instance.shap_values.return_value = np.array([[0.2, 0.3]])
            
            # Call the function with forced phase "early"
            result = explain_student(student_data, forced_phase="early")
            
            # Assertions
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 2)
            
            # Verify open was called at least once, and that one of the calls has the expected arguments
            mock_open_instance.assert_called()
            path_match_found = False
            for call_args in mock_open_instance.call_args_list:
                args, kwargs = call_args
                if args and 'models/early/artifacts/random_forest_model.pkl' in args:
                    path_match_found = True
                    break
            self.assertTrue(path_match_found, "Expected path not found in open() calls")
    
    @patch('os.path.exists')
    def test_explain_student_insufficient_data(self, mock_path_exists):
        """Test explain_student function with insufficient data"""
        # Mock path exists
        mock_path_exists.return_value = True
        
        # Create student data with insufficient fields
        student_data = {
            'gender': 'F',  # Missing other required fields
        }
        
        # Call the function and check for ValueError
        with self.assertRaises(ValueError) as context:
            explain_student(student_data)
        
        self.assertIn("Not enough data", str(context.exception))
    
    def test_explain_student_missing_model(self):
        """Test explain_student function with missing model file"""
        # Create valid student data
        student_data = {
            'student_number': '12345',
            'gender': 0,
            'age_at_enrollment': 20,
        }
        
        # Use patching context manager for better control
        with patch('models.utils.system.shap_explainer.EARLY_FIELDS', ['student_number', 'gender', 'age_at_enrollment']), \
             patch('os.path.exists', return_value=False):
            
            # Call the function and check for FileNotFoundError
            with self.assertRaises(FileNotFoundError) as context:
                explain_student(student_data)
            
            # Check that the error message contains "Model not found"
            self.assertIn("Model not found", str(context.exception))
    
    def test_explain_student_multi_class_model(self):
        """Test explain_student function with a multi-class model"""
        # Create valid student data
        student_data = {
            'student_number': '12345',
            'gender': 0,
            'age_at_enrollment': 18,
        }
        
        # Use context managers for patching instead of decorators
        with patch('models.utils.system.shap_explainer.EARLY_FIELDS', 
                  ['student_number', 'gender', 'age_at_enrollment']), \
             patch('models.utils.system.shap_explainer._model_cache', {}), \
             patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open()) as mock_file_open, \
             patch('pickle.load') as mock_pickle_load, \
             patch('models.utils.system.shap_explainer.preprocess_row_for_inference') as mock_preprocess, \
             patch('shap.TreeExplainer') as mock_tree_explainer:
                
            # Mock model
            mock_model = MagicMock()
            mock_model.feature_names_in_ = ['feature1', 'feature2']
            mock_pickle_load.return_value = mock_model
            
            # Mock preprocessed data
            mock_df = pd.DataFrame({
                'feature1': [0.5],
                'feature2': [0.7]
            })
            mock_preprocess.return_value = mock_df
            
            # Mock SHAP explainer
            mock_explainer = MagicMock()
            mock_tree_explainer.return_value = mock_explainer
            
            # Mock multi-class SHAP values (list of arrays for each class)
            mock_shap_values = [np.array([[0.1, 0.2]]), np.array([[0.3, 0.4]])]
            mock_explainer.shap_values.return_value = mock_shap_values
            
            # Call the function
            result = explain_student(student_data)
            
            # Assertions
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 2)
            self.assertEqual(result['feature1'], 0.1)
            self.assertEqual(result['feature2'], 0.2)
            
            # The file should be opened at least once with a path containing "early"
            # Check for any call containing the path pattern
            found_call = False
            for call_args in mock_file_open.mock_calls:
                if len(call_args.args) >= 1:
                    if 'models/early/artifacts/random_forest_model.pkl' in str(call_args.args[0]):
                        found_call = True
                        break
            
            # Assert that we found a call with the expected path
            self.assertTrue(found_call, "Expected file path not found in open() calls")


if __name__ == '__main__':
    unittest.main() 