import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from db.database import Base
from db.models import Student, RiskPrediction
from api.main import app
from api.deps import get_db

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_risk.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

@pytest.fixture
def setup_database():
    """Set up a test database with a student and risk prediction."""
    # Create tables
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
        student_number="888888",
        first_name="Risk",
        last_name="Student",
        gender=1,
        marital_status=1,
        previous_qualification_grade=14.0,
        admission_grade=142.5,
        displaced=False,
        debtor=False,
        tuition_fees_up_to_date=True,
        scholarship_holder=False,
        age_at_enrollment=19,
        curricular_units_1st_sem_enrolled=6,
        curricular_units_1st_sem_approved=6,
        curricular_units_1st_sem_grade=14.0,
        curricular_units_2nd_sem_grade=13.5
    )
    db.add(test_student)
    
    # Add an existing risk prediction
    timestamp = datetime.now()
    test_prediction = RiskPrediction(
        student_number="888888",
        risk_score=0.25,
        risk_level="low",
        model_phase="early",
        timestamp=timestamp
    )
    db.add(test_prediction)
    
    db.commit()
    db.close()
    
    yield
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_create_risk_prediction(setup_database):
    """Test creating a new risk prediction."""
    # Use Python datetime object directly - don't convert to string
    current_time = datetime.now()
    
    prediction_data = {
        "student_number": "888888",
        "risk_score": 0.75,
        "risk_level": "moderate",
        "model_phase": "mid",
        # Don't send timestamp in request - let server generate it
    }
    
    response = client.post("/api/risk-predictions/", json=prediction_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["student_number"] == prediction_data["student_number"]
    assert data["risk_level"] == prediction_data["risk_level"]
    assert data["model_phase"] == prediction_data["model_phase"]


def test_get_latest_prediction(setup_database):
    """Test retrieving the latest risk prediction for a student."""
    response = client.get("/api/risk-predictions/latest/888888")
    
    assert response.status_code == 200
    data = response.json()
    assert data["student_number"] == "888888"
    assert "risk_level" in data
    assert "model_phase" in data
    assert "timestamp" in data


def test_get_predictions_by_student(setup_database):
    """Test retrieving all predictions for a specific student."""
    # Add an additional prediction for the same student
    prediction_data = {
        "student_number": "888888",
        "risk_score": 0.85,
        "risk_level": "high",
        "model_phase": "final",
        # Let server generate timestamp
    }
    
    client.post("/api/risk-predictions/", json=prediction_data)
    
    # Now get all predictions for this student
    response = client.get("/api/risk-predictions/student/888888")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Should have at least 2 predictions now
    
    # Check if predictions are sorted by timestamp (newest first)
    for i in range(len(data) - 1):
        timestamp1 = datetime.fromisoformat(data[i]["timestamp"].replace("Z", "+00:00"))
        timestamp2 = datetime.fromisoformat(data[i+1]["timestamp"].replace("Z", "+00:00"))
        assert timestamp1 >= timestamp2


def test_get_predictions_by_phase(setup_database):
    """Test retrieving predictions filtered by phase."""
    response = client.get("/api/risk-predictions/phase/early")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    # All returned predictions should be for the early phase
    for prediction in data:
        assert prediction["model_phase"] == "early"


def test_download_predictions(setup_database):
    """Test downloading risk predictions as CSV."""
    response = client.get("/api/download/predictions")
    
    assert response.status_code == 200
    assert "text/csv" in response.headers["Content-Type"]
    assert "attachment; filename=risk_predictions.csv" in response.headers["Content-Disposition"]
    
    # Basic check on CSV content
    content = response.content.decode('utf-8')
    assert "student_number" in content
    assert "risk_level" in content
    assert "888888" in content 