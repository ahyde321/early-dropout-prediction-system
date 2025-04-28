import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Importing the modules to test
from models.utils.system.formatting import to_snake_case
from models.utils.system.model_info import (
    get_model_path, get_test_data_path, load_model, 
    get_feature_importance, get_model_metrics, get_model_info
)

class TestFormattingUtils(unittest.TestCase):
    """Tests for the formatting utilities"""
    
    def test_to_snake_case(self):
        """Test to_snake_case function with various inputs"""
        # Basic conversion
        self.assertEqual(to_snake_case("Hello World"), "hello_world")
        
        # Already snake case
        self.assertEqual(to_snake_case("hello_world"), "hello_world")
        
        # Camel case
        self.assertEqual(to_snake_case("HelloWorld"), "helloworld")
        
        # With spaces, dashes, and slashes
        self.assertEqual(to_snake_case("Hello-World/Test"), "hello_world_test")
        
        # With special characters
        self.assertEqual(to_snake_case("Hello World! @#$"), "hello_world")
        
        # Multiple spaces/underscores
        self.assertEqual(to_snake_case("Hello   World___Test"), "hello_world_test")
        
        # Leading/trailing underscores
        self.assertEqual(to_snake_case("__Hello_World__"), "hello_world")
        
        # Empty string
        self.assertEqual(to_snake_case(""), "")
        
        # Whitespace only
        self.assertEqual(to_snake_case("   "), "")


class TestModelInfoUtils(unittest.TestCase):
    """Tests for the model_info utilities"""
    
    def test_get_model_path(self):
        """Test get_model_path function"""
        # Default base directory
        expected_path = "models/early/artifacts/random_forest_model.pkl"
        self.assertEqual(get_model_path("early"), expected_path)
        
        # Custom base directory
        custom_base = "/custom/models"
        expected_path = "/custom/models/mid/artifacts/random_forest_model.pkl"
        self.assertEqual(get_model_path("mid", custom_base), expected_path)
    
    def test_get_test_data_path(self):
        """Test get_test_data_path function"""
        # Default base directory
        expected_path = "models/early/artifacts/test_data.pkl"
        self.assertEqual(get_test_data_path("early"), expected_path)
        
        # Custom base directory
        custom_base = "/custom/models"
        expected_path = "/custom/models/final/artifacts/test_data.pkl"
        self.assertEqual(get_test_data_path("final", custom_base), expected_path)
    
    @patch('os.path.exists')
    @patch('pickle.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_model(self, mock_file_open, mock_pickle_load, mock_path_exists):
        """Test load_model function"""
        # Setup mocks
        mock_path_exists.return_value = True
        mock_model = MagicMock()
        mock_pickle_load.return_value = mock_model
        
        # Call the function
        result = load_model("early")
        
        # Assertions
        self.assertEqual(result, mock_model)
        mock_file_open.assert_called_once_with("models/early/artifacts/random_forest_model.pkl", "rb")
        
        # Test with non-existent model
        mock_path_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            load_model("nonexistent")
    
    
    def test_get_feature_importance_unsupported_model(self):
        """Test get_feature_importance with a model that has neither feature_importances_ nor coef_"""
        # Create a mock model with neither attribute
        model = MagicMock()
        model.feature_names_in_ = np.array(['feature1', 'feature2'])
        
        # Get feature importances
        importances = get_feature_importance(model)
        
        # Assertions
        self.assertIsInstance(importances, dict)
        self.assertEqual(len(importances), 0)  # Empty dict
    
    @patch('os.path.exists')
    @patch('joblib.load')
    @patch('models.utils.system.model_info.load_model')
    def test_get_model_metrics(self, mock_load_model, mock_joblib_load, mock_path_exists):
        """Test get_model_metrics function"""
        # Setup mocks
        mock_path_exists.return_value = True
        
        # Create mock test data
        X_test = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
        y_test = np.array([0, 1, 0])
        mock_joblib_load.return_value = (X_test, y_test)
        
        # Create mock model
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([0, 1, 0])  # Perfect predictions
        mock_load_model.return_value = mock_model
        
        # Call the function
        metrics = get_model_metrics("early")
        
        # Assertions
        self.assertIsInstance(metrics, dict)
        self.assertEqual(metrics["accuracy"], 1.0)  # Perfect accuracy
        self.assertEqual(metrics["precision"], 1.0)
        self.assertEqual(metrics["recall"], 1.0)
        self.assertEqual(metrics["f1_score"], 1.0)
        
        # Test with non-existent test data
        mock_path_exists.return_value = False
        warning_metrics = get_model_metrics("nonexistent")
        self.assertIn("warning", warning_metrics)
    
    @patch('models.utils.system.model_info.load_model')
    @patch('models.utils.system.model_info.get_model_metrics')
    @patch('models.utils.system.model_info.get_feature_importance')
    def test_get_model_info_single_phase(self, mock_get_importance, mock_get_metrics, mock_load_model):
        """Test get_model_info function with a single phase"""
        # Setup mocks
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model
        
        mock_metrics = {"accuracy": 0.9, "precision": 0.85}
        mock_get_metrics.return_value = mock_metrics
        
        mock_importance = {"feature1": 0.7, "feature2": 0.3}
        mock_get_importance.return_value = mock_importance
        
        # Call the function
        result = get_model_info("early")
        
        # Assertions
        self.assertIsInstance(result, dict)
        self.assertIn("early", result)
        self.assertEqual(result["early"]["metrics"], mock_metrics)
        self.assertEqual(result["early"]["feature_importance"], mock_importance)
        
        # Verify mock calls
        mock_load_model.assert_called_once_with("early", "models/")
        mock_get_metrics.assert_called_once_with("early", "models/")
        mock_get_importance.assert_called_once_with(mock_model)
    
    @patch('models.utils.system.model_info.load_model')
    def test_get_model_info_nonexistent_model(self, mock_load_model):
        """Test get_model_info function with a non-existent model"""
        # Setup mocks
        mock_load_model.side_effect = FileNotFoundError("Model not found")
        
        # Call the function
        result = get_model_info("nonexistent")
        
        # Assertions
        self.assertIsInstance(result, dict)
        self.assertIn("nonexistent", result)
        self.assertIn("error", result["nonexistent"])
        self.assertIn("Model not found", result["nonexistent"]["error"])


if __name__ == '__main__':
    unittest.main() 