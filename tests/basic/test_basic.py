# tests/test_students_routes.py

from fastapi.testclient import TestClient
from api.main import app  # wherever you create your FastAPI app

client = TestClient(app)

def test_create_student():
    payload = {
        "student_number": "b2cecdc4",
        "first_name": "Gary",
        "last_name": "Savage",
        "age_at_enrollment": 18,
        "application_order": 1,
        "curricular_units_1st_sem_enrolled": 6,
        "daytime_evening_attendance": 1,
        "debtor": 0,
        "displaced": 1,
        "gender": 0,
        "marital_status": 1,
        "scholarship_holder": 0,
        "tuition_fees_up_to_date": 1,
        "curricular_units_1st_sem_approved": 1,
        "curricular_units_1st_sem_grade": 12
    }

    response = client.post("/api/students/create", json=payload)
    assert response.status_code in [200, 422]  # 422 if missing fields

def test_get_student_by_number():
    response = client.get("/api/students/by-number/S12345")
    assert response.status_code in [200, 404]

def test_update_student():
    update_payload = {
        "first_name": "Updated"
    }
    response = client.patch("/api/students/S12345", json=update_payload)
    assert response.status_code in [200, 404]

def test_get_all_students():
    response = client.get("/api/students/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_download_students():
    response = client.get("/api/download/students")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]

def test_get_student_status():
    response = client.get("/api/students/S12345/status")
    assert response.status_code in [200, 404]

def test_get_student_history():
    response = client.get("/api/students/S12345/history")
    assert response.status_code in [200, 404]

def test_get_distinct_values_valid():
    response = client.get("/api/students/distinct-values?field=gender")
    assert response.status_code == 200

def test_get_distinct_values_invalid():
    response = client.get("/api/students/distinct-values?field=invalid_field")
    assert response.status_code == 200
    assert "error" in response.json()

def test_get_students_with_notes():
    response = client.get("/api/students/with-notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_risk_summary_by_phase():
    response = client.get("/api/students/summary-by-phase")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_risk_summary_by_phase_with_filter():
    response = client.get("/api/students/summary-by-phase?filter_field=gender&filter_value=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "early" in data
    assert "mid" in data
    assert "final" in data

def test_get_nonexistent_student():
    response = client.get("/api/students/by-number/nonexistent123")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_update_nonexistent_student():
    update_payload = {"first_name": "ShouldNotWork"}
    response = client.patch("/api/students/nonexistent123", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_create_student_missing_fields():
    payload = {
        "student_number": "missingfields"
        # Missing many required fields
    }
    response = client.post("/api/students/create", json=payload)
    assert response.status_code == 422

def test_get_distinct_invalid_field():
    response = client.get("/api/students/distinct-values?field=invalid_field")
    assert response.status_code == 200
    assert "error" in response.json()

def test_get_nonexistent_student_history():
    response = client.get("/api/students/nonexistent123/history")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_get_nonexistent_student_status():
    response = client.get("/api/students/nonexistent123/status")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"
