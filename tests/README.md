# API Tests

This directory contains unit tests for validating the functionality of the API endpoints.

## Tests Overview

- `test_student_routes.py`: Tests for student-related API endpoints in `api/routes/students.py`
- `test_prediction_routes.py`: Tests for prediction-related API endpoints in `api/routes/prediction.py`

## Running the Tests

To run the tests, make sure you have pytest installed:

```bash
pip install pytest
```

Then run the tests from the project root directory:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_student_routes.py
pytest tests/test_prediction_routes.py

# Run with verbose output
pytest -v tests/

# Run a specific test
pytest tests/test_student_routes.py::test_get_student_by_number
```

## Test Design

Each test file follows a similar structure:

1. **Setup**: Creates an in-memory SQLite database and populates it with test data
2. **Override dependencies**: Redirects database connections to the test database
3. **Test cases**: One test per API endpoint to validate functionality

The tests use pytest fixtures to manage the database lifecycle, ensuring each test runs with a clean database state.

## Mocking

For prediction functionality, we mock the machine learning models to avoid requiring the actual model files during testing. This allows us to test the API behavior independently of the model implementation.

## Test Coverage

These tests validate that each endpoint:

1. Returns the expected status code
2. Returns data in the expected format
3. Properly handles error cases (e.g., not found)
4. Correctly interacts with the database

Note that these tests focus on API functionality and do not test the actual machine learning models or prediction algorithms. 