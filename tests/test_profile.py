import pytest
from app import create_app
from extensions import db
from models.user import User
from flask_login import login_user

@pytest.fixture
def app():
    app = create_app('testing')  # Create the app with the testing config
    yield app
    with app.app_context():
        db.drop_all()  # Drop all tables after the test
        db.create_all()  # Create new tables for the next test

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def add_test_user(app):
    with app.app_context():
        # Create and add a test user to the database
        hashed_password = 'hashed_password'  # This should be hashed in a real test
        user = User(username='testuser', password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return user

def test_user_can_view_own_profile(client, add_test_user):
    with client:
        # Log in the test user
        login_user(add_test_user)
        
        # Visit the profile page (assuming this route exists)
        response = client.get('/profile')  # Change '/profile' to your actual route

        # Assert that the user is redirected to the correct page or can see their profile data
        assert response.status_code == 200
        assert b"testuser" in response.data  # Check if the username is in the response
        # You can assert other profile elements like profile picture if required
