import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch
from datetime import datetime

from db.database import Base, get_db
from api.main import app
from db.models import Student, RiskPrediction
from tests.utils import mock_predict_student, mock_explain_student

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the app's dependency with our test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    """Set up a fresh test database for each test."""
    # Create the database tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create test data
    db = TestingSessionLocal()
    
    # Add a simple test student
    test_student = Student(
        student_number="12345", 
        first_name="Test", 
        last_name="Student",
        gender=1,
        marital_status=1,
        previous_qualification_grade=14.0,
        admission_grade=142.5,
        displaced=0,
        debtor=0,
        tuition_fees_up_to_date=1,
        scholarship_holder=0,
        age_at_enrollment=19,
        curricular_units_1st_sem_enrolled=6,
        curricular_units_1st_sem_approved=6,
        curricular_units_1st_sem_grade=14.0,
        curricular_units_2nd_sem_grade=13.5
    )
    db.add(test_student)
    
    # Add a simple risk prediction
    test_prediction = RiskPrediction(
        student_number="12345",
        risk_score=0.3,
        risk_level="low",
        model_phase="early",
        timestamp=datetime(2023, 1, 1, 12, 0, 0),
        shap_values={"feature1": 0.1, "feature2": -0.2}
    )
    db.add(test_prediction)
    db.commit()
    db.close()
    
    yield
    
    # Clean up (drop tables)
    Base.metadata.drop_all(bind=engine)

# Basic test for predicting all students
@pytest.mark.usefixtures("setup_database")
@patch("models.utils.system.prediction.predict_student", side_effect=mock_predict_student)
@patch("models.utils.system.shap_explainer.explain_student", side_effect=mock_explain_student)
def test_bulk_predict_all_students(mock_explain, mock_predict):
    """Test predicting for all students."""
    response = client.get("/api/predict/all")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "predictions" in data
    assert "skipped" in data
    assert isinstance(data["predictions"], list)
    assert isinstance(data["skipped"], list)


# Basic test for downloading predictions
@pytest.mark.usefixtures("setup_database")
def test_download_predictions():
    """Test downloading predictions as CSV."""
    response = client.get("/api/download/predictions")
    
    assert response.status_code == 200
    assert "text/csv" in response.headers["Content-Type"]
    assert "attachment; filename=predictions.csv" in response.headers["Content-Disposition"]
    
    # Basic check on CSV content
    content = response.content.decode('utf-8')
    assert "student_number" in content
    assert "12345" in content

# Add a test for recalculate-all endpoint
@pytest.mark.usefixtures("setup_database")
@patch("models.utils.system.prediction.predict_student", side_effect=mock_predict_student)
@patch("models.utils.system.shap_explainer.explain_student", side_effect=mock_explain_student)
def test_recalculate_all_predictions(mock_explain, mock_predict):
    """Test recalculating predictions for all students."""
    response = client.get("/api/predict/recalculate-all")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "predictions_updated_or_created" in data
    assert "skipped" in data
    assert isinstance(data["predictions_updated_or_created"], list)
    assert isinstance(data["skipped"], list)

