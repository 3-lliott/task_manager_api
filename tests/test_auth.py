def test_signup_success(client):
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "elliot",
            "password": "password123"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "elliot"
    assert data["role"] == "user"


def test_signup_duplicate_username(client):
    payload = {
        "username": "elliot",
        "password": "password123"
    }

    client.post("/api/v1/auth/signup", json=payload)

    response = client.post(
        "/api/v1/auth/signup",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_signup_invalid_data(client):
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "ab",
            "password": "123"
        },
    )

    assert response.status_code == 422


def test_login_success(client):
    client.post(
        "/api/v1/auth/signup",
        json={
            "username": "elliot",
            "password": "password123"
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "elliot",
            "password": "password123"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/signup",
        json={
            "username": "elliot",
            "password": "password123"
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "elliot",
            "password": "wrongpassword"
        },
    )

    assert response.status_code == 401