# tests/basic/test_students_basic.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime

from api.main import app
from db.models import Student, RiskPrediction

client = TestClient(app)

# Sample data for tests
mock_student1 = {
    "student_number": "b2cecdc4",
    "first_name": "Gary",
    "last_name": "Savage",
    "age_at_enrollment": 18,
    "marital_status": 1,
    "previous_qualification_grade": 14.0,
    "admission_grade": 140.0,
    "curricular_units_1st_sem_enrolled": 6,
    "debtor": 0,
    "displaced": 1,
    "gender": 0,
    "scholarship_holder": 0,
    "tuition_fees_up_to_date": 1,
    "curricular_units_1st_sem_approved": 1,
    "curricular_units_1st_sem_grade": 12.0,
    "risk_trend": "↑"
}

mock_student2 = {
    "student_number": "c3defd5e",
    "first_name": "Alice",
    "last_name": "Johnson",
    "age_at_enrollment": 19,
    "marital_status": 0,
    "previous_qualification_grade": 15.0,
    "admission_grade": 145.0,
    "curricular_units_1st_sem_enrolled": 5,
    "debtor": 0,
    "displaced": 0,
    "gender": 1,
    "scholarship_holder": 1,
    "tuition_fees_up_to_date": 1,
    "curricular_units_1st_sem_approved": 2,
    "curricular_units_1st_sem_grade": 14.0,
    "notes": "This student needs additional support in mathematics.",
    "risk_trend": "→"
}

mock_prediction1 = {
    "student_number": "b2cecdc4",
    "risk_score": 0.9,
    "risk_level": "high",
    "model_phase": "early",
    "timestamp": datetime.utcnow().isoformat()
}

# === POSITIVE TEST CASES (HAPPY PATH) ===

@patch("api.routes.students.get_db")
def test_get_existing_student(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Mock the student object that would be returned from the database
    mock_student_obj = MagicMock()
    for key, value in mock_student1.items():
        setattr(mock_student_obj, key, value)
    
    # Configure the mock query to return our mock student when filtered by student_number
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student_obj
    
    # Make the request
    response = client.get("/api/students/by-number/b2cecdc4")
    
    # Verify the response
    assert response.status_code == 200
    assert response.json()["student_number"] == "b2cecdc4"

@patch("api.routes.students.get_db")
def test_update_existing_student(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Mock the student object that would be returned from the database
    mock_student_obj = MagicMock()
    for key, value in mock_student1.items():
        setattr(mock_student_obj, key, value)
    
    # Configure the mock query to return our mock student when filtered by student_number
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student_obj
    
    # Make the request with update data
    update_payload = {"first_name": "UpdatedName"}
    response = client.patch("/api/students/b2cecdc4", json=update_payload)
    
    # Verify the response
    assert response.status_code == 200
    assert response.json()["message"] == "Student updated"
    
    # Verify that the student object was updated and the DB was committed
    assert mock_student_obj.first_name == "UpdatedName"
    assert mock_db.commit.called

@patch("api.routes.students.get_db")
def test_get_all_students(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Mock student objects
    mock_students = []
    for student_data in [mock_student1, mock_student2]:
        student_obj = MagicMock()
        for key, value in student_data.items():
            setattr(student_obj, key, value)
        mock_students.append(student_obj)
    
    # Configure the mock to return our list of students
    mock_db.query.return_value.all.return_value = mock_students
    mock_db.query.return_value.outerjoin.return_value.all.return_value = []  # For trend calculation
    
    # Make the request
    response = client.get("/api/students/list")
    
    # Verify the response
    assert response.status_code == 200
    students = response.json()
    assert isinstance(students, list)
    assert len(students) == 2
    assert any(s["student_number"] == "b2cecdc4" for s in students)
    assert any(s["student_number"] == "c3defd5e" for s in students)
    # Check that risk_trend is included in the student data
    assert any("risk_trend" in s for s in students)

@patch("api.routes.students.get_db")
def test_download_students(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Mock student objects
    mock_students = []
    for student_data in [mock_student1, mock_student2]:
        student_obj = MagicMock()
        for key, value in student_data.items():
            setattr(student_obj, key, value)
        mock_students.append(student_obj)
    
    # Configure the mock to return our list of students
    mock_db.query.return_value.all.return_value = mock_students
    
    # Make the request
    response = client.get("/api/download/students")
    
    # Verify the response
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]

@patch("api.routes.students.get_db")
def test_get_distinct_values_valid(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Configure the mock to return distinct values
    mock_query = mock_db.query.return_value.distinct.return_value
    mock_query.all.return_value = [(0,), (1,)]
    
    # Make the request
    response = client.get("/api/students/distinct-values?field=gender")
    
    # Verify the response
    assert response.status_code == 200
    distinct = response.json()
    assert isinstance(distinct, list)
    assert len(distinct) == 2
    assert 0 in distinct
    assert 1 in distinct

@patch("api.routes.students.get_db")
def test_get_students_with_notes(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Mock student objects with notes
    mock_student_obj = MagicMock()
    for key, value in mock_student2.items():
        setattr(mock_student_obj, key, value)
    
    # Configure the mock to return our list of students with notes
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_student_obj]
    
    # Make the request
    response = client.get("/api/students/with-notes")
    
    # Verify the response
    assert response.status_code == 200
    notes = response.json()
    assert isinstance(notes, list)
    assert len(notes) == 1
    assert notes[0]["student_number"] == "c3defd5e"
    assert "This student needs additional support in mathematics." in notes[0]["reason"]

@patch("api.routes.students.get_db")
def test_get_student_status_existing(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Mock the student object
    mock_student_obj = MagicMock()
    for key, value in mock_student1.items():
        setattr(mock_student_obj, key, value)
    
    # Mock the prediction object
    mock_prediction_obj = MagicMock()
    for key, value in mock_prediction1.items():
        setattr(mock_prediction_obj, key, value)
    
    # Configure the mocks
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student_obj
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_prediction_obj
    
    # Make the request
    response = client.get("/api/students/b2cecdc4/status")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert "student" in data
    assert "latest_prediction" in data
    assert data["student"]["student_number"] == "b2cecdc4"
    assert data["latest_prediction"]["risk_level"] == "high"

@patch("api.routes.students.get_db")
def test_get_student_history_existing(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Mock the student object
    mock_student_obj = MagicMock()
    for key, value in mock_student1.items():
        setattr(mock_student_obj, key, value)
    
    # Mock the prediction objects
    mock_prediction_obj = MagicMock()
    for key, value in mock_prediction1.items():
        setattr(mock_prediction_obj, key, value)
    
    # Configure the mocks
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student_obj
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_prediction_obj]
    
    # Make the request
    response = client.get("/api/students/b2cecdc4/history")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert "student" in data
    assert "predictions" in data
    assert data["student"]["student_number"] == "b2cecdc4"
    assert len(data["predictions"]) == 1
    assert data["predictions"][0]["risk_level"] == "high"

@patch("api.routes.students.get_db")
def test_get_risk_summary_by_phase_no_filter(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Configure the mock to return risk summaries
    mock_db.execute.return_value.fetchall.return_value = [
        ("early", "high", 2),
        ("early", "moderate", 1),
        ("mid", "high", 1),
        ("mid", "low", 2),
        ("final", "moderate", 2),
        ("final", "low", 1)
    ]
    
    # Make the request
    response = client.get("/api/students/summary-by-phase")
    
    # Verify the response
    assert response.status_code == 200
    summary = response.json()
    assert "early" in summary
    assert "mid" in summary
    assert "final" in summary
    assert summary["early"]["high"] == 2
    assert summary["mid"]["low"] == 2
    assert summary["final"]["moderate"] == 2

# === NEGATIVE TEST CASES (UNHAPPY PATH) ===

@patch("api.routes.students.get_db")
def test_get_nonexistent_student(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Configure the mock to return None for a nonexistent student
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    response = client.get("/api/students/by-number/nonexistent")
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

@patch("api.routes.students.get_db")
def test_update_nonexistent_student(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Configure the mock to return None for a nonexistent student
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    update_payload = {"first_name": "ShouldNotWork"}
    response = client.patch("/api/students/nonexistent", json=update_payload)
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

@patch("api.routes.students.get_db")
def test_get_student_status_nonexistent(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Configure the mock to return None for a nonexistent student
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    response = client.get("/api/students/nonexistent/status")
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

@patch("api.routes.students.get_db")
def test_get_student_history_nonexistent(mock_get_db):
    # Mock the database session and query results
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Configure the mock to return None for a nonexistent student
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    response = client.get("/api/students/nonexistent/history")
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

@patch("api.routes.students.get_db")
def test_get_distinct_values_invalid(mock_get_db):
    # Mock the database session
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Make the request with an invalid field
    response = client.get("/api/students/distinct-values?field=invalid_field")
    
    # Verify the response
    assert response.status_code == 200
    assert "error" in response.json()

@patch("api.routes.students.get_db")
def test_get_risk_summary_invalid_filter(mock_get_db):
    # Mock the database session
    mock_db = MagicMock()
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # Make the request with an invalid filter field
    response = client.get("/api/students/summary-by-phase?filter_field=invalid&filter_value=something")
    
    # Verify the response
    assert response.status_code == 200
    assert "error" in response.json()
