import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime

from db.database import Base, get_db
from api.main import app
from db.models import Student, RiskPrediction

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the app's dependency with our test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def setup_database():
    """Set up a test database with a student and risk prediction."""
    # Drop all tables to reset the schema
    Base.metadata.drop_all(bind=engine)
    
    # Create tables based on the current models
    Base.metadata.create_all(bind=engine)
    
    # Override the dependency to use our test database
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Add test data
    db = TestingSessionLocal()
    
    # Add a test student
    test_student = Student(
        student_number="999999",
        first_name="New",
        last_name="Student",
        gender=1,
        marital_status=1,
        age_at_enrollment=20,
        scholarship_holder=False,
        tuition_fees_up_to_date=True,
        previous_qualification_grade=14.5,
        admission_grade=140.0,
        debtor=False,
        displaced=False,
        curricular_units_1st_sem_enrolled=6,
        curricular_units_1st_sem_approved=4,
        curricular_units_1st_sem_grade=13.0,
        curricular_units_2nd_sem_grade=12.5
    )
    db.add(test_student)
    
    # Add a test risk prediction
    test_prediction = RiskPrediction(
        student_number="999999",
        risk_score=0.2,
        risk_level="low",
        model_phase="early",
        timestamp=datetime.now()
    )
    db.add(test_prediction)
    
    db.commit()
    db.close()
    
    yield
    
    # Clean up after tests
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

# Basic test for creating a student
def test_create_student(setup_database):
    """Test creating a new student."""
    student_data = {
        "student_number": "99999",
        "first_name": "New",
        "last_name": "Student",
        "gender": 1,  # Using integer for gender
        "marital_status": 1,
        "age_at_enrollment": 20,
        "scholarship_holder": False,
        "tuition_fees_up_to_date": True,
        "previous_qualification_grade": 14.5,
        "admission_grade": 140.0,
        "debtor": False,
        "displaced": False,
        "curricular_units_1st_sem_enrolled": 6
    }
    
    response = client.post("/api/students/create", json=student_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["student_number"] == student_data["student_number"]
    assert data["first_name"] == student_data["first_name"]

# Basic test for getting a student by number
def test_get_student_by_number(setup_database):
    """Test retrieving a student by their student number."""
    response = client.get("/api/students/by-number/999999")
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "New"
    assert data["last_name"] == "Student"

# Basic test for updating a student
def test_update_student(setup_database):
    """Test updating a student's information."""
    update_data = {
        "notes": "Updated notes"
    }
    
    response = client.patch("/api/students/999999", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Student updated"
    assert data["student"] == "999999"

# Basic test for listing all students
def test_get_all_students(setup_database):
    """Test retrieving all students."""
    response = client.get("/api/students/list")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    # Check if our test student is in the results
    found = False
    for student in data:
        if student["student_number"] == "999999":
            found = True
            assert student["first_name"] == "New"
            assert student["last_name"] == "Student"
            break
    
    assert found, "Test student not found in results"

# Basic test for downloading students as CSV
def test_download_students(setup_database):
    """Test downloading student data as CSV."""
    response = client.get("/api/download/students")
    
    assert response.status_code == 200
    assert "text/csv" in response.headers["Content-Type"]
    assert "attachment; filename=students.csv" in response.headers["Content-Disposition"]
    
    # Basic check on CSV content
    content = response.content.decode('utf-8')
    assert "student_number" in content
    assert "999999" in content

# Basic test for getting a student's status
def test_get_student_status(setup_database):
    """Test retrieving a student's current status."""
    response = client.get("/api/students/999999/status")
    
    assert response.status_code == 200
    data = response.json()
    assert "student" in data
    assert data["student"]["student_number"] == "999999"
    assert "latest_prediction" in data

# Basic test for getting a student's prediction history
def test_get_student_history(setup_database):
    """Test retrieving a student's prediction history."""
    response = client.get("/api/students/999999/history")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_get_distinct_values(setup_database):
    """Test retrieving distinct values for a field."""
    response = client.get("/api/students/distinct-values?field=marital_status")
    
    assert response.status_code == 200
    data = response.json()
    # Using integer values as in the real database
    assert 1 in data  # 1 might represent "Single" in the database

def test_get_students_with_notes(setup_database):
    """Test retrieving students who have notes."""
    # First add notes to our test student
    update_data = {"notes": "Test notes"}
    client.patch("/api/students/999999", json=update_data)
    
    response = client.get("/api/students/with-notes")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check if our test student is in the results
    found = False
    for student in data:
        if student["student_number"] == "999999":
            found = True
            break
    
    assert found, "Test student with notes not found"

def test_get_risk_summary_by_phase(setup_database):
    """Test retrieving risk level summary grouped by phase."""
    response = client.get("/api/students/summary-by-phase")
    
    assert response.status_code == 200
    data = response.json()
    
    # Since we have a low risk student in the early phase
    assert "early" in data
    assert "low" in data["early"]
    # Don't assert exact counts since there may be other data in the DB
    assert data["early"]["low"] > 0

def test_get_risk_summary_by_phase_with_filter(setup_database):
    """Test retrieving filtered risk level summary."""
    response = client.get("/api/students/summary-by-phase?filter_field=gender&filter_value=1")
    
    assert response.status_code == 200
    data = response.json()
    
    # Our test student is gender=1 and has low risk in early phase
    assert "early" in data
    assert "low" in data["early"]
    assert data["early"]["low"] > 0