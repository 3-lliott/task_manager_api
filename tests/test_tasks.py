def test_create_task_success(client, auth_headers):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Learn pytest",
            "description": "Write tests"
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn pytest"
    assert data["completed"] is False
    assert data["category_id"] is None


def test_create_task_invalid_category(client, auth_headers):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Bad task",
            "category_id": 999
        },
        headers=auth_headers,
    )

    assert response.status_code == 400


def test_create_task_unauthenticated(client):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Unauthorized task"
        },
    )

    assert response.status_code == 401


def test_create_task_invalid_title(client, auth_headers):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "   "
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_get_all_tasks(client, auth_headers):
    client.post(
        "/api/v1/tasks",
        json={"title": "My task"},
        headers=auth_headers,
    )

    response = client.get(
        "/api/v1/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_all_tasks_unauthenticated(client):
    response = client.get("/api/v1/tasks")

    assert response.status_code == 401


def test_get_task(client, task, auth_headers):
    response = client.get(
        f"/api/v1/tasks/{task['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_get_task_not_found(client, auth_headers):
    response = client.get(
        "/api/v1/tasks/999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_task_forbidden(client, task, second_user_headers):
    response = client.get(
        f"/api/v1/tasks/{task['id']}",
        headers=second_user_headers,
    )

    assert response.status_code == 403


def test_update_task(client, task, auth_headers):
    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={
            "title": "Updated task",
            "completed": True
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated task"
    assert data["completed"] is True


def test_update_task_unassociate_category(
    client,
    category,
    auth_headers
):
    created = client.post(
        "/api/v1/tasks",
        json={
            "title": "Categorized task",
            "category_id": category["id"]
        },
        headers=auth_headers,
    )

    task_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={
            "category_id": None
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["category_id"] is None


def test_update_task_invalid_category(
    client,
    task,
    auth_headers
):
    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={
            "category_id": 999
        },
        headers=auth_headers,
    )

    assert response.status_code == 400


def test_update_task_not_found(client, auth_headers):
    response = client.patch(
        "/api/v1/tasks/999",
        json={"title": "Updated"},
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_update_task_forbidden(
    client,
    task,
    second_user_headers
):
    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={"title": "Hacked"},
        headers=second_user_headers,
    )

    assert response.status_code == 403


def test_delete_task(client, task, auth_headers):
    response = client.delete(
        f"/api/v1/tasks/{task['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_delete_task_not_found(client, auth_headers):
    response = client.delete(
        "/api/v1/tasks/999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_delete_task_forbidden(
    client,
    task,
    second_user_headers
):
    response = client.delete(
        f"/api/v1/tasks/{task['id']}",
        headers=second_user_headers,
    )

    assert response.status_code == 403