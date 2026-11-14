def test_admin_get_tasks(
    client,
    admin_headers,
    auth_headers
):
    client.post(
        "/api/v1/tasks",
        json={"title": "User task"},
        headers=auth_headers,
    )

    response = client.get(
        "/api/v1/admin/tasks",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_admin_get_tasks_forbidden(
    client,
    auth_headers
):
    response = client.get(
        "/api/v1/admin/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 403


def test_admin_get_tasks_unauthenticated(client):
    response = client.get(
        "/api/v1/admin/tasks"
    )

    assert response.status_code == 401