# tests/conftest.py

import sys
from pathlib import Path

# Dynamically find the project root (2 levels up from this file)
project_root = Path(__file__).resolve().parents[1]

# Add the project root to sys.path if not already present
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from fastapi.testclient import TestClient
from api.main import app
from tests.test_database import TestingSessionLocal, setup_test_db
from api.routes.students import get_db  # <-- IMPORTANT: import your real get_db

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override once, before tests run
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def initialize_test_db():
    """Set up the test database once before all tests."""
    setup_test_db()
    yield
    # No teardown needed for in-memory database

@pytest.fixture(scope="module")
def test_client():
    """Fixture to get a test client with overridden DB."""
    return TestClient(app)
