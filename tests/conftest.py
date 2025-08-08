import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app

from app.models.user import User
from app.utils.auth import hash_password

# Ganti URL ini dengan database test kamu
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Terapkan override
app.dependency_overrides[get_db] = override_get_db

# Fixture client test
@pytest.fixture(scope="module")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def user_token_headers(client):
    db = next(override_get_db())
    user = User(
        username="normaluser",
        email="user@example.com",
        password=hash_password("userpass"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    login_response = client.post("/auth/login", json={
        "username": "normaluser",
        "password": "userpass"
    })

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def test_user(client, admin_token_headers):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass",
        "role": "user"
    }
    response = client.post("/users", json=user_data, headers=admin_token_headers)
    return response.json()
