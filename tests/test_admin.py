from conftest import create_user


def test_admin_get_all_tasks(client, admin_headers, auth_headers):
    client.post(
        "/api/v1/tasks",
        json={"title": "User task"},
        headers=auth_headers,
    )

    response = client.get(
        "/api/v1/tasks",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "User task"


def test_user_gets_only_own_tasks(client, auth_headers, second_user_headers):
    client.post(
        "/api/v1/tasks",
        json={"title": "First user's task"},
        headers=auth_headers,
    )

    client.post(
        "/api/v1/tasks",
        json={"title": "Second user's task"},
        headers=second_user_headers,
    )

    response = client.get(
        "/api/v1/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "First user's task"


def test_unauthenticated_get_tasks(client):
    response = client.get("/api/v1/tasks")

    assert response.status_code == 401


def test_admin_can_make_user_admin(client, db, admin_headers):
    user = create_user(
        db,
        username="newuser",
        password="password123"
    )

    response = client.patch(
        f"/api/v1/users/{user.id}/admin",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_non_admin_cannot_make_user_admin(client, db, auth_headers):
    user = create_user(
        db,
        username="newuser",
        password="password123"
    )

    response = client.patch(
        f"/api/v1/users/{user.id}/admin",
        headers=auth_headers
    )

    assert response.status_code == 403