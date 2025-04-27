import os
import unittest
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock, mock_open

# Main functions we want to test
from models.utils.system.prediction import predict_student, get_risk_level
from models.utils.system.preprocessing import preprocess_row_for_inference
from models.utils.system.shap_explainer import explain_student
from models.utils.predictor import load_model, predict_new_data
from models.utils.analysis_tools import (
    load_data, clean_data, summarize_data, analyze_dropout_factors
)

class TestPredictionModule(unittest.TestCase):
    """Tests for the prediction.py module"""
    
    @patch('os.path.exists')
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('models.utils.system.preprocessing.preprocess_row_for_inference')
    def test_predict_student_early_phase(self, mock_preprocess, mock_file_open, mock_pickle_load, mock_path_exists):
        """Test predict_student function for early phase prediction"""
        # Setup mocks
        mock_path_exists.return_value = True
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['age_at_enrollment', 'application_order', 
                                      'curricular_units_1st_sem_enrolled', 
                                      'daytime_evening_attendance', 'debtor',
                                      'displaced', 'gender', 'marital_status',
                                      'scholarship_holder', 'tuition_fees_up_to_date']
        mock_model.predict_proba.return_value = np.array([[0.3, 0.7]])
        mock_pickle_load.return_value = mock_model
        mock_preprocess.return_value = pd.DataFrame([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 
                                                  columns=mock_model.feature_names_in_)
        
        # Student data
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
            'application_order': 1,
            'daytime_evening_attendance': 1
        }
        
        # Test with return_phase=False
        result = predict_student(student_data)
        self.assertEqual(result, 0.7)
        
        # Test with return_phase=True
        result, phase = predict_student(student_data, return_phase=True)
        self.assertEqual(result, 0.7)
        self.assertEqual(phase, 'early')
        
        # Verify mocks were called correctly
        mock_preprocess.assert_called_once()
        mock_model.predict_proba.assert_called_once()
    
    def test_get_risk_level(self):
        """Test get_risk_level function"""
        self.assertEqual(get_risk_level(0.2), "low")
        self.assertEqual(get_risk_level(0.4), "low")
        self.assertEqual(get_risk_level(0.5), "moderate")
        self.assertEqual(get_risk_level(0.7), "moderate")
        self.assertEqual(get_risk_level(0.8), "high")
        self.assertEqual(get_risk_level(1.0), "high")


class TestPreprocessingModule(unittest.TestCase):
    """Tests for the preprocessing.py module"""
    
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_preprocess_row_for_inference(self, mock_file_open, mock_pickle_load):
        """Test preprocess_row_for_inference function"""
        # Setup mocks
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['age_at_enrollment', 'gender', 'marital_status']
        
        mock_label_encoders = {'gender': MagicMock()}
        mock_label_encoders['gender'].transform.return_value = np.array([1])
        mock_label_encoders['gender'].classes_ = ['male', 'female']
        
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([[0.5, 0.5]])
        
        # Configure pickle.load to return different objects on consecutive calls
        mock_pickle_load.side_effect = [mock_label_encoders, mock_scaler]
        
        # Input data
        data = {
            'age_at_enrollment': 20,
            'gender': 'male',
            'marital_status': 1
        }
        
        # Call the function
        result = preprocess_row_for_inference(data, 'fake_model_dir', mock_model)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ['age_at_enrollment', 'gender', 'marital_status'])
        self.assertEqual(len(result), 1)  # One row
        
        # Verify that the scaler was applied to numerical columns
        mock_scaler.transform.assert_called_once()
        
        # Verify that label encoder was used for categorical columns
        mock_label_encoders['gender'].transform.assert_called_once_with(['male'])


class TestShapExplainerModule(unittest.TestCase):
    """Tests for the shap_explainer.py module"""
    
    @patch('os.path.exists')
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('models.utils.system.preprocessing.preprocess_row_for_inference')
    @patch('shap.TreeExplainer')
    def test_explain_student(self, mock_tree_explainer, mock_preprocess, 
                             mock_file_open, mock_pickle_load, mock_path_exists):
        """Test explain_student function"""
        # Setup mocks
        mock_path_exists.return_value = True
        mock_model = MagicMock()
        mock_model.feature_names_in_ = ['age_at_enrollment', 'gender', 'marital_status']
        mock_pickle_load.return_value = mock_model
        
        mock_explainer = MagicMock()
        mock_tree_explainer.return_value = mock_explainer
        
        # Mock the preprocessed DataFrame
        mock_df = pd.DataFrame([[20, 1, 1]], columns=['age_at_enrollment', 'gender', 'marital_status'])
        mock_preprocess.return_value = mock_df
        
        # Mock the SHAP values
        mock_shap_values = np.array([[0.1, 0.2, -0.3]])
        mock_explainer.shap_values.return_value = mock_shap_values
        
        # Student data
        student_data = {
            'student_number': '12345',
            'first_name': 'Test',
            'last_name': 'Student',
            'marital_status': 1,
            'gender': 1,
            'age_at_enrollment': 20,
            'curricular_units_1st_sem_enrolled': 6,
            'application_order': 1,
            'daytime_evening_attendance': 1,
            'debtor': 0,
            'displaced': 1,
            'scholarship_holder': 0,
            'tuition_fees_up_to_date': 1
        }
        
        # Call the function
        result = explain_student(student_data, forced_phase='early')
        
        # Assertions
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 3)  # Three features
        self.assertEqual(result['age_at_enrollment'], 0.1)
        self.assertEqual(result['gender'], 0.2)
        self.assertEqual(result['marital_status'], -0.3)
        
        # Verify mocks were called correctly
        mock_preprocess.assert_called_once()
        mock_explainer.shap_values.assert_called_once_with(mock_df)


class TestPredictorModule(unittest.TestCase):
    """Tests for the predictor.py module"""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('pickle.load')
    def test_load_model(self, mock_pickle_load, mock_file_open):
        """Test load_model function"""
        mock_model = MagicMock()
        mock_pickle_load.return_value = mock_model
        
        result = load_model('fake_model_path')
        
        self.assertEqual(result, mock_model)
        mock_file_open.assert_called_once_with('fake_model_path', 'rb')
        mock_pickle_load.assert_called_once()
    
    @patch('os.path.exists')
    @patch('pandas.read_csv')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pickle.load')
    @patch('pandas.DataFrame.to_csv')
    def test_predict_new_data(self, mock_to_csv, mock_pickle_load, 
                             mock_file_open, mock_read_csv, mock_path_exists):
        """Test predict_new_data function"""
        # Setup mocks
        mock_path_exists.return_value = True
        mock_model = MagicMock()
        mock_pickle_load.return_value = mock_model
        
        # Mock the input data
        mock_input_data = pd.DataFrame({
            'feature1': [1, 2, 3],
            'feature2': [4, 5, 6]
        })
        mock_read_csv.return_value = mock_input_data
        
        # Mock the predictions
        mock_model.predict.return_value = np.array([0, 1, 0])
        
        # Call the function
        result = predict_new_data('fake_model_path', 'fake_data_path', 'fake_output_path')
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)  # Three rows
        self.assertEqual(list(result.columns), ['Predicted Outcome'])
        
        # Verify mocks were called correctly
        mock_read_csv.assert_called_once_with('fake_data_path')
        mock_model.predict.assert_called_once_with(mock_input_data)
        mock_to_csv.assert_called_once_with('fake_output_path', index=False)


class TestAnalysisToolsModule(unittest.TestCase):
    """Tests for the analysis_tools.py module"""
    
    @patch('pandas.read_csv')
    def test_load_data(self, mock_read_csv):
        """Test load_data function"""
        mock_df = pd.DataFrame({'col1': [1, 2, 3]})
        mock_read_csv.return_value = mock_df
        
        result = load_data('fake_filepath')
        
        self.assertEqual(result.equals(mock_df), True)
        mock_read_csv.assert_called_once_with('fake_filepath')
    
    def test_clean_data(self):
        """Test clean_data function"""
        # Create a DataFrame with missing values
        df = pd.DataFrame({
            'col1': [1, 2, None, 4],
            'col2': [5, None, 7, 8]
        })
        
        result = clean_data(df)
        
        # Assertions
        self.assertEqual(len(result), 2)  # Two rows left after dropping NaN
        self.assertEqual(result.isnull().sum().sum(), 0)  # No NaN values
    
    def test_summarize_data(self):
        """Test summarize_data function"""
        df = pd.DataFrame({
            'col1': [1, 2, 3, 4],
            'col2': [5, 6, 7, 8]
        })
        
        result = summarize_data(df)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (8, 2))  # 8 stats for 2 columns
        # Check for expected statistics
        self.assertIn('count', result.index)
        self.assertIn('mean', result.index)
        self.assertIn('std', result.index)
        
    def test_analyze_dropout_factors(self):
        """Test analyze_dropout_factors function"""
        df = pd.DataFrame({
            'Predicted Label': ['Dropout', 'Graduate', 'Dropout', 'Graduate'],
            'age': [20, 22, 21, 23],
            'gender': [0, 1, 0, 1],
            'grade': [60, 80, 65, 85]
        })
        
        result = analyze_dropout_factors(df)
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 3)  # 3 features
        self.assertEqual(result.columns.tolist(), [False, True])  # False=Graduate, True=Dropout


if __name__ == '__main__':
    unittest.main() 