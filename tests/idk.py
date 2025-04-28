import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from api.routes.students import router
from db.models import Student
from api.schemas import StudentSchema, StudentCreate
from fastapi import FastAPI

# filepath: /Users/andrewhyde/workspace/gitlab.com/ahyde03/finalProject/api/routes/test_students.py

app = FastAPI()
app.include_router(router)

client = TestClient(app)

# Mock database session
@pytest.fixture
def mock_db_session():
    with patch("api.routes.students.SessionLocal") as mock_session:
        yield mock_session

def test_create_student_success(mock_db_session):
    # Arrange
    mock_db = MagicMock()
    mock_db_session.return_value = mock_db
    student_data = {
        "student_number": "12345",
        "first_name": "John",
        "last_name": "Doe",
        "age": 20
    }
    mock_student = Student(**student_data)
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_student

    # Act
    response = client.post("/students/create", json=student_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["student_number"] == "12345"

def test_create_student_failure(mock_db_session):
    # Arrange
    mock_db = MagicMock()
    mock_db_session.return_value = mock_db
    student_data = {
        "student_number": "12345",
        "first_name": "John",
        "last_name": "Doe",
        "age": 20
    }
    mock_db.add.side_effect = Exception("Database error")

    # Act
    response = client.post("/students/create", json=student_data)

    # Assert
    assert response.status_code == 500

def test_get_student_by_number_success(mock_db_session):
    # Arrange
    mock_db = MagicMock()
    mock_db_session.return_value = mock_db
    student_data = {
        "student_number": "12345",
        "first_name": "John",
        "last_name": "Doe",
        "age": 20
    }
    mock_student = Student(**student_data)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # Act
    response = client.get("/students/by-number/12345")

    # Assert
    assert response.status_code == 200
    assert response.json()["student_number"] == "12345"

def test_get_student_by_number_not_found(mock_db_session):
    # Arrange
    mock_db = MagicMock()
    mock_db_session.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.get("/students/by-number/12345")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"