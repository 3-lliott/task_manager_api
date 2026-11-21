def test_create_category_success(client, admin_headers):
    response = client.post(
        "/api/v1/categories",
        json={
            "name": "Work",
            "description": "Work-related tasks"
        },
        headers=admin_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Work"
    assert data["description"] == "Work-related tasks"


def test_create_category_duplicate(client, admin_headers):
    client.post(
        "/api/v1/categories",
        json={"name": "Work"},
        headers=admin_headers,
    )

    response = client.post(
        "/api/v1/categories",
        json={"name": "Work"},
        headers=admin_headers,
    )

    assert response.status_code == 400


def test_create_category_invalid_name(client, admin_headers):
    response = client.post(
        "/api/v1/categories",
        json={"name": ""},
        headers=admin_headers,
    )

    assert response.status_code == 422


def test_get_categories(client, category, auth_headers):
    response = client.get(
        "/api/v1/categories",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_categories_empty(client, auth_headers):
    response = client.get(
        "/api/v1/categories",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_category(client, category, auth_headers):
    response = client.get(
        f"/api/v1/categories/{category['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Work"


def test_get_category_not_found(client, auth_headers):
    response = client.get(
        "/api/v1/categories/999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_update_category(client, category, admin_headers):
    response = client.put(
        f"/api/v1/categories/{category['id']}",
        json={
            "name": "Updated Work",
            "description": "Updated description"
        },
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Work"


def test_update_category_not_found(client, admin_headers):
    response = client.put(
        "/api/v1/categories/999",
        json={
            "name": "Work",
            "description": "Work-related tasks"
        },
        headers=admin_headers,
    )

    assert response.status_code == 404


def test_update_category_duplicate(client, category, admin_headers):
    client.post(
        "/api/v1/categories",
        json={"name": "Personal"},
        headers=admin_headers,
    )

    response = client.put(
        f"/api/v1/categories/{category['id']}",
        json={"name": "Personal"},
        headers=admin_headers,
    )

    assert response.status_code == 400


def test_delete_category(client, category, admin_headers):
    response = client.delete(
        f"/api/v1/categories/{category['id']}",
        headers=admin_headers,
    )

    assert response.status_code == 200


def test_delete_category_not_found(client, admin_headers):
    response = client.delete(
        "/api/v1/categories/999",
        headers=admin_headers,
    )

    assert response.status_code == 404


def test_get_category_tasks(client, category, auth_headers, admin_headers):
    client.post(
        "/api/v1/tasks",
        json={
            "title": "Category task",
            "category_id": category["id"]
        },
        headers=auth_headers,
    )

    response = client.get(
        f"/api/v1/categories/{category['id']}/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_category_tasks_not_found(client, auth_headers):
    response = client.get(
        "/api/v1/categories/999/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 404