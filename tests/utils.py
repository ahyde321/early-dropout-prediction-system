"""
Testing utilities for mocking dependencies.
"""

def mock_predict_student(student_data, return_phase=False):
    """
    Mock implementation of predict_student for testing.
    """
    if return_phase:
        # Return (raw_score, phase)
        return 0.25, "early"
    return 0.25  # Just return a raw score

def mock_explain_student(student_data):
    """
    Mock implementation of explain_student for testing.
    """
    return {"feature1": 0.3, "feature2": -0.5}  # Mock SHAP values 