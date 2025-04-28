import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
from io import BytesIO

from api.main import app
from api.routes.uploads import get_db
from db.models import Student

# Setup client
client = TestClient(app)

def get_test_csv_file(data):
    """Helper to create a CSV file from a list of dictionaries."""
    df = pd.DataFrame(data)
    return BytesIO(df.to_csv(index=False).encode('utf-8'))

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup before each test and teardown after"""
    # Setup
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    yield mock_db
    # Teardown
    app.dependency_overrides.clear()

def test_upload_grades(setup_and_teardown):
    """Test uploading grades CSV and updating student records."""
    mock_db = setup_and_teardown
    
    # Sample grade data
    grade_data = [
        {
            "student_number": "123456",
            "curricular_units_1st_sem_approved": 5,
            "curricular_units_1st_sem_grade": 15.5,
            "curricular_units_2nd_sem_grade": 16.0
        },
        {
            "student_number": "789012",
            "curricular_units_1st_sem_approved": 4,
            "curricular_units_1st_sem_grade": 14.0,
            "curricular_units_2nd_sem_grade": 15.0
        }
    ]

    # Create a test CSV file
    test_file = get_test_csv_file(grade_data)

    # Configure mock database behavior
    mock_student1 = MagicMock()
    mock_student2 = MagicMock()
    
    # Set up query chain to return our mock students
    mock_filter1 = MagicMock()
    mock_filter1.first.return_value = mock_student1
    
    mock_filter2 = MagicMock()
    mock_filter2.first.return_value = mock_student2
    
    # Mock query.filter() to return different filters based on condition
    mock_query = MagicMock()
    mock_query.filter.side_effect = [mock_filter1, mock_filter2]
    mock_db.query.return_value = mock_query
    
    # Make the request
    with patch('api.routes.uploads.pd.read_csv', return_value=pd.DataFrame(grade_data)):
        files = {"file": ("grades.csv", test_file, "text/csv")}
        response = client.post("/api/upload/grades", files=files)
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify database operations
        assert mock_db.commit.called
        assert len(mock_query.filter.call_args_list) >= 1

def test_upload_grades_student_not_found(setup_and_teardown):
    """Test uploading grades CSV with a non-existent student."""
    mock_db = setup_and_teardown
    
    # Sample grade data with one non-existent student
    grade_data = [
        {
            "student_number": "123456",  # Exists
            "curricular_units_1st_sem_approved": 5,
            "curricular_units_1st_sem_grade": 15.5
        },
        {
            "student_number": "999999",  # Doesn't exist
            "curricular_units_1st_sem_approved": 4,
            "curricular_units_1st_sem_grade": 14.0
        }
    ]

    # Create a test CSV file
    test_file = get_test_csv_file(grade_data)

    # Configure mock database behavior
    mock_student = MagicMock()
    
    # Set up query chain to return our mock student for 123456, and None for 999999
    mock_filter1 = MagicMock()
    mock_filter1.first.return_value = mock_student
    
    mock_filter2 = MagicMock()
    mock_filter2.first.return_value = None
    
    # Mock query.filter() to return different filters based on condition
    mock_query = MagicMock()
    mock_query.filter.side_effect = [mock_filter1, mock_filter2]
    mock_db.query.return_value = mock_query
    
    # Make the request
    with patch('api.routes.uploads.pd.read_csv', return_value=pd.DataFrame(grade_data)):
        files = {"file": ("grades.csv", test_file, "text/csv")}
        response = client.post("/api/upload/grades", files=files)
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify database operations
        assert mock_db.commit.called
        assert len(mock_query.filter.call_args_list) >= 1

def test_upload_students(setup_and_teardown):
    """Test bulk uploading new students."""
    mock_db = setup_and_teardown
    
    # Sample student data
    student_data = [
        {
            "student_number": "S001",
            "first_name": "John",
            "last_name": "Doe",
            "gender": 1,
            "email": "john.doe@example.com"
        },
        {
            "student_number": "S002",
            "first_name": "Jane",
            "last_name": "Smith",
            "gender": 2,
            "email": "jane.smith@example.com"
        }
    ]

    # Create a test CSV file
    test_file = get_test_csv_file(student_data)

    # Set up query to indicate no existing students
    mock_filter = MagicMock()
    mock_filter.first.return_value = None
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query
    
    # Make the request
    with patch('api.routes.uploads.Student') as MockStudent:
        with patch('api.routes.uploads.pd.read_csv', return_value=pd.DataFrame(student_data)):
            files = {"file": ("students.csv", test_file, "text/csv")}
            response = client.post("/api/upload/students", files=files)
            
            # Verify the response
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "message" in data
            assert "added" in data
            assert "skipped" in data
            assert "failed" in data
            assert "details" in data
            
            # Verify database operations
            assert mock_db.add.called
            assert mock_db.commit.called

def test_upload_students_duplicate(setup_and_teardown):
    """Test handling of duplicate student numbers during bulk upload."""
    mock_db = setup_and_teardown
    
    # Sample student data with one duplicate
    student_data = [
        {
            "student_number": "S001",
            "first_name": "John",
            "last_name": "Doe",
            "gender": 1,
            "email": "john.doe@example.com"
        },
        {
            "student_number": "S002",  # This one will be a duplicate
            "first_name": "Jane",
            "last_name": "Smith",
            "gender": 2,
            "email": "jane.smith@example.com"
        }
    ]

    # Create a test CSV file
    test_file = get_test_csv_file(student_data)

    # Create mock to simulate existing student check
    def filter_side_effect(condition):
        mock_filter = MagicMock()
        if "Student.student_number = :student_number_1" in str(condition):
            # For S001
            mock_filter.first.return_value = None
        else:
            # For S002
            mock_existing = MagicMock()
            mock_existing.student_number = "S002"
            mock_filter.first.return_value = mock_existing
        return mock_filter
        
    mock_query = MagicMock()
    mock_query.filter.side_effect = filter_side_effect
    mock_db.query.return_value = mock_query
    
    # Make the request
    with patch('api.routes.uploads.Student') as MockStudent:
        with patch('api.routes.uploads.pd.read_csv', return_value=pd.DataFrame(student_data)):
            files = {"file": ("students.csv", test_file, "text/csv")}
            response = client.post("/api/upload/students", files=files)
            
            # Verify the response
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "message" in data
            assert "added" in data
            assert "skipped" in data
            assert "failed" in data
            assert "details" in data
            
            # Verify database operations - the operation completed
            assert mock_db.commit.called

def test_upload_students_missing_required_fields(setup_and_teardown):
    """Test uploading students with missing required fields."""
    mock_db = setup_and_teardown
    
    # Sample student data with missing required fields
    student_data = [
        {
            "student_number": "S001",  # Missing first_name and last_name
            "gender": 1,
            "email": "john.doe@example.com"
        }
    ]

    # Create a test CSV file
    test_file = get_test_csv_file(student_data)
    
    # Make the request with mocked pd.read_csv
    with patch('api.routes.uploads.pd.read_csv', return_value=pd.DataFrame(student_data)):
        files = {"file": ("students.csv", test_file, "text/csv")}
        response = client.post("/api/upload/students", files=files)
        
        # Verify the response has an error about missing fields
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "required" in data["detail"].lower()

def test_upload_invalid_file_type(setup_and_teardown):
    """Test uploading a non-CSV file type."""
    mock_db = setup_and_teardown
    
    # Create a text file instead of CSV
    test_file = BytesIO(b"This is not a CSV file")
    
    # Make the request with our invalid test file
    files = {"file": ("invalid.txt", test_file, "text/plain")}
    response = client.post("/api/upload/students", files=files)
    
    # Verify the response indicates invalid file type error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "csv" in data["detail"].lower() 