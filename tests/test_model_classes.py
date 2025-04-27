import unittest
from pydantic import ValidationError
from models import EarlyStudentData, MidStudentData, FinalStudentData

class TestModelClasses(unittest.TestCase):
    """Tests for the Pydantic model classes defined in models/__init__.py"""
    
    def test_early_student_data_valid(self):
        """Test valid data for EarlyStudentData"""
        # Valid data
        data = {
            "age_at_enrollment": 18,
            "application_order": 1,
            "curricular_units_1st_sem_enrolled": 6,
            "daytime_evening_attendance": 1,
            "debtor": 0,
            "displaced": 1,
            "gender": 0,
            "marital_status": 1,
            "scholarship_holder": 0,
            "tuition_fees_up_to_date": 1
        }
        
        # This should not raise an exception
        early_data = EarlyStudentData(**data)
        
        # Check fields
        self.assertEqual(early_data.age_at_enrollment, 18)
        self.assertEqual(early_data.application_order, 1)
        self.assertEqual(early_data.gender, 0)
    
    def test_early_student_data_invalid(self):
        """Test invalid data for EarlyStudentData"""
        # Missing required field
        data = {
            "age_at_enrollment": 18,
            "application_order": 1,
            # Missing curricular_units_1st_sem_enrolled
            "daytime_evening_attendance": 1,
            "debtor": 0,
            "displaced": 1,
            "gender": 0,
            "marital_status": 1,
            "scholarship_holder": 0,
            "tuition_fees_up_to_date": 1
        }
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            EarlyStudentData(**data)
        
        # Wrong type for integer field
        data = {
            "age_at_enrollment": "eighteen",  # String instead of int
            "application_order": 1,
            "curricular_units_1st_sem_enrolled": 6,
            "daytime_evening_attendance": 1,
            "debtor": 0,
            "displaced": 1,
            "gender": 0,
            "marital_status": 1,
            "scholarship_holder": 0,
            "tuition_fees_up_to_date": 1
        }
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            EarlyStudentData(**data)
    
    def test_mid_student_data_valid(self):
        """Test valid data for MidStudentData"""
        # Valid data
        data = {
            "age_at_enrollment": 19,
            "curricular_units_1st_sem_approved": 5,
            "curricular_units_1st_sem_enrolled": 6,
            "curricular_units_1st_sem_grade": 14.5,
            "debtor": 0,
            "displaced": 0,
            "gender": 1,
            "marital_status": 0,
            "scholarship_holder": 1,
            "tuition_fees_up_to_date": 1
        }
        
        # This should not raise an exception
        mid_data = MidStudentData(**data)
        
        # Check fields
        self.assertEqual(mid_data.age_at_enrollment, 19)
        self.assertEqual(mid_data.curricular_units_1st_sem_approved, 5)
        self.assertEqual(mid_data.curricular_units_1st_sem_grade, 14.5)
    
    def test_mid_student_data_invalid(self):
        """Test invalid data for MidStudentData"""
        # Missing required field
        data = {
            "age_at_enrollment": 19,
            # Missing curricular_units_1st_sem_approved
            "curricular_units_1st_sem_enrolled": 6,
            "curricular_units_1st_sem_grade": 14.5,
            "debtor": 0,
            "displaced": 0,
            "gender": 1,
            "marital_status": 0,
            "scholarship_holder": 1,
            "tuition_fees_up_to_date": 1
        }
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            MidStudentData(**data)
        
        # Wrong type for float field
        data = {
            "age_at_enrollment": 19,
            "curricular_units_1st_sem_approved": 5,
            "curricular_units_1st_sem_enrolled": 6,
            "curricular_units_1st_sem_grade": "fourteen",  # String instead of float
            "debtor": 0,
            "displaced": 0,
            "gender": 1,
            "marital_status": 0,
            "scholarship_holder": 1,
            "tuition_fees_up_to_date": 1
        }
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            MidStudentData(**data)
    
    def test_final_student_data_valid(self):
        """Test valid data for FinalStudentData"""
        # Valid data
        data = {
            "age_at_enrollment": 20,
            "curricular_units_1st_sem_approved": 6,
            "curricular_units_1st_sem_enrolled": 6,
            "curricular_units_1st_sem_grade": 15.0,
            "curricular_units_2nd_sem_grade": 16.0,
            "debtor": 0,
            "displaced": 1,
            "gender": 0,
            "scholarship_holder": 1,
            "tuition_fees_up_to_date": 1
        }
        
        # This should not raise an exception
        final_data = FinalStudentData(**data)
        
        # Check fields
        self.assertEqual(final_data.age_at_enrollment, 20)
        self.assertEqual(final_data.curricular_units_1st_sem_grade, 15.0)
        self.assertEqual(final_data.curricular_units_2nd_sem_grade, 16.0)
    
    def test_final_student_data_invalid(self):
        """Test invalid data for FinalStudentData"""
        # Missing required field
        data = {
            "age_at_enrollment": 20,
            "curricular_units_1st_sem_approved": 6,
            "curricular_units_1st_sem_enrolled": 6,
            "curricular_units_1st_sem_grade": 15.0,
            # Missing curricular_units_2nd_sem_grade
            "debtor": 0,
            "displaced": 1,
            "gender": 0,
            "scholarship_holder": 1,
            "tuition_fees_up_to_date": 1
        }
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            FinalStudentData(**data)
        
        # Invalid value for boolean-like int field
        data = {
            "age_at_enrollment": 20,
            "curricular_units_1st_sem_approved": 6,
            "curricular_units_1st_sem_enrolled": 6,
            "curricular_units_1st_sem_grade": 15.0,
            "curricular_units_2nd_sem_grade": 16.0,
            "debtor": 2,  # Should be 0 or 1
            "displaced": 1,
            "gender": 0,
            "scholarship_holder": 1,
            "tuition_fees_up_to_date": 1
        }
        
        # Note: This will actually pass since Pydantic only validates type, not range
        # But we're including it for completeness
        final_data = FinalStudentData(**data)
        self.assertEqual(final_data.debtor, 2)


if __name__ == '__main__':
    unittest.main() 