import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auth import hash_password
from database import Base, get_db
from main import app
from models import User


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def create_user(
    db,
    username="testuser",
    password="password123",
    role="user"
):
    user = User(
        username=username,
        hashed_password=hash_password(password),
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/api/v1/auth/signup",
        json={
            "username": "testuser",
            "password": "password123"
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture()
def second_user_headers(client):
    client.post(
        "/api/v1/auth/signup",
        json={
            "username": "seconduser",
            "password": "password123"
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "seconduser",
            "password": "password123"
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture()
def admin_headers(client, db):
    create_user(
        db,
        username="admin",
        password="admin123",
        role="admin"
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin",
            "password": "admin123"
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture()
def category(client):
    response = client.post(
        "/api/v1/categories",
        json={
            "name": "Work",
            "description": "Work-related tasks"
        },
    )

    return response.json()


@pytest.fixture()
def task(client, auth_headers):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test task",
            "description": "A task for testing"
        },
        headers=auth_headers,
    )

    return response.json()