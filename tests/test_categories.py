def test_create_category_success(client):
    response = client.post(
        "/api/v1/categories",
        json={
            "name": "Work",
            "description": "Work tasks"
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Work"


def test_create_category_duplicate(client):
    payload = {
        "name": "Work",
        "description": "Work tasks"
    }

    client.post("/api/v1/categories", json=payload)

    response = client.post(
        "/api/v1/categories",
        json=payload
    )

    assert response.status_code == 400


def test_create_category_invalid_name(client):
    response = client.post(
        "/api/v1/categories",
        json={
            "name": "   "
        },
    )

    assert response.status_code == 422


def test_get_categories(client, category):
    response = client.get("/api/v1/categories")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_categories_empty(client):
    response = client.get("/api/v1/categories")

    assert response.status_code == 200
    assert response.json() == []


def test_get_category(client, category):
    response = client.get(
        f"/api/v1/categories/{category['id']}"
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Work"


def test_get_category_not_found(client):
    response = client.get(
        "/api/v1/categories/999"
    )

    assert response.status_code == 404


def test_update_category(client, category):
    response = client.put(
        f"/api/v1/categories/{category['id']}",
        json={
            "name": "Personal",
            "description": "Personal tasks"
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Personal"


def test_update_category_not_found(client):
    response = client.put(
        "/api/v1/categories/999",
        json={
            "name": "Personal"
        },
    )

    assert response.status_code == 404


def test_update_category_duplicate(client, category):
    client.post(
        "/api/v1/categories",
        json={"name": "Personal"}
    )

    response = client.put(
        f"/api/v1/categories/{category['id']}",
        json={"name": "Personal"},
    )

    assert response.status_code == 400


def test_delete_category(client, category):
    response = client.delete(
        f"/api/v1/categories/{category['id']}"
    )

    assert response.status_code == 200


def test_delete_category_not_found(client):
    response = client.delete(
        "/api/v1/categories/999"
    )

    assert response.status_code == 404


def test_get_category_tasks(client, category, auth_headers):
    client.post(
        "/api/v1/tasks",
        json={
            "title": "Categorized task",
            "category_id": category["id"]
        },
        headers=auth_headers,
    )

    response = client.get(
        f"/api/v1/categories/{category['id']}/tasks"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_category_tasks_not_found(client):
    response = client.get(
        "/api/v1/categories/999/tasks"
    )

    assert response.status_code == 404