import pytest
from app import create_app
from extensions import db

# Fixture to create and configure the app for testing
@pytest.fixture
def app():
    app = create_app('testing')  # Use the testing configuration
    with app.app_context():
        db.create_all()  # Create the database tables
        yield app  # Yield the app to the test function
        db.session.remove()  # Ensure any ongoing database session is removed
        db.drop_all()  # Drop all tables after the test

# Fixture to provide a test client for simulating HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()
