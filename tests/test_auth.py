import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
import tempfile
import os

# Create a temporary database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAuthentication:
    """Test suite for authentication endpoints"""
    
    def test_register_user_success(self):
        """Test successful user registration"""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "testpassword123",
                "name": "Test User",
                "username": "testuser"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert data["username"] == "testuser"
        assert "id" in data
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email fails"""
        # First registration
        client.post(
            "/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "testpassword123",
                "name": "First User"
            }
        )
        
        # Second registration with same email
        response = client.post(
            "/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "testpassword123",
                "name": "Second User"
            }
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_login_success(self):
        """Test successful login"""
        # Register user first
        client.post(
            "/auth/register",
            json={
                "email": "login@example.com",
                "password": "testpassword123",
                "name": "Login User"
            }
        )
        
        # Login
        response = client.post(
            "/auth/login",
            data={
                "username": "login@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials fails"""
        response = client.post(
            "/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 400
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_get_current_user_without_token(self):
        """Test accessing protected endpoint without token fails"""
        response = client.get("/users/me")
        assert response.status_code == 401
    
    def test_get_current_user_with_token(self):
        """Test accessing protected endpoint with valid token succeeds"""
        # Register and login
        client.post(
            "/auth/register",
            json={
                "email": "protected@example.com",
                "password": "testpassword123",
                "name": "Protected User"
            }
        )
        
        login_response = client.post(
            "/auth/login",
            data={
                "username": "protected@example.com",
                "password": "testpassword123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Access protected endpoint
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "protected@example.com" 