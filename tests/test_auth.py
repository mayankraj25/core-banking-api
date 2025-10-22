from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User

# The 'client' fixture is imported automatically by pytest
# from your test setup file.

def test_register_user_success(client: TestClient):
    """
    Test successful user registration.
    """
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone": "1234567890",
            "password": "strongpassword123"
        }
    )
    
    # Check that the request was successful
    assert response.status_code == 200
    
    # Check the response data
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert "id" in data
    
    # CRUCIAL: Check that the password hash is NOT returned
    assert "hashed_password" not in data

def test_register_user_duplicate_email(client: TestClient):
    """
    Test that registering with a duplicate email fails.
    """
    # Create the first user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123"
        }
    )
    
    # Try to create a second user with the same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "first_name": "Another",
            "last_name": "Person",
            "password": "password456"
        }
    )
    
    # Check that the API returns a 400 Bad Request error
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_user_success(client: TestClient):
    """
    Test successful user login.
    """
    # 1. Create a user to log in with
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "first_name": "Login",
            "last_name": "User",
            "password": "loginpass123"
        }
    )
    
    # 2. Try to log in
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "loginpass123"
        }
    )
    
    # Check for a successful response
    assert response.status_code == 200
    
    # Check that a token was returned
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_fail(client: TestClient):
    """
    Test login with a wrong password.
    """
    # 1. Create a user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "fail@example.com",
            "first_name": "Login",
            "last_name": "User",
            "password": "correctpassword"
        }
    )
    
    # 2. Try to log in with the wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "fail@example.com",
            "password": "wrongpassword"
        }
    )
    
    # Check for a 401 Unauthorized error
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"