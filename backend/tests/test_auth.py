import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
 
from app.main import app
from app.models import Base
from app.dependencies import get_db
from app.models import User
from app.auth import hash_password
 
# Use the test database URL from environment
TEST_DB = os.environ["DATABASE_URL"]
engine = create_engine(TEST_DB)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
 
@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
 
 
@pytest.fixture
def db():
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
 
 
@pytest.fixture
def client(db):
    """Test client that uses the test database session."""
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
 
 
@pytest.fixture
def admin_user(db):
    user = User(
        email="admin@test.com",
        hashed_password=hash_password("testpass123"),
        is_admin=True,
    )
    db.add(user)
    db.commit()
    return user
 
 
def test_login_success(client, admin_user):
    response = client.post(
        "/auth/login",
        data={"username": "admin@test.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
 
 
def test_login_wrong_password(client, admin_user):
    response = client.post(
        "/auth/login",
        data={"username": "admin@test.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
 
 
def test_students_requires_auth(client):
    response = client.get("/students/")
    assert response.status_code == 401
 
 
def test_list_students_authenticated(client, admin_user):
    # Log in first
    login = client.post(
        "/auth/login",
        data={"username": "admin@test.com", "password": "testpass123"},
    )
    token = login.json()["access_token"]
 
    # Now fetch students
    response = client.get(
        "/students/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
