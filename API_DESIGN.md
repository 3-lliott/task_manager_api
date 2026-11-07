# API Design

## Base URL

```text
http://127.0.0.1:8000/api/v1
```

## Authentication

The API uses JWT Bearer authentication.

- Users register with a username and password.
- Passwords are hashed before being stored.
- Login returns an access token.
- Protected endpoints require an `Authorization: Bearer <token>` header.
- New accounts receive the `user` role by default.

## Endpoints

### Authentication

| Method | Endpoint       | Description          | Authentication |
| ------ | -------------- | -------------------- | -------------- |
| POST   | `/auth/signup` | Register a user      | Public         |
| POST   | `/auth/login`  | Login and obtain JWT | Public         |

**Signup request:**

```json
{
  "username": "elliot",
  "password": "password123"
}
```

**Login:** Accepts form data containing `username` and `password`.

**Successful login response:**

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

### Tasks

| Method | Endpoint           | Description             | Authentication |
| ------ | ------------------ | ----------------------- | -------------- |
| POST   | `/tasks`           | Create a task           | Required       |
| GET    | `/tasks`           | Get accessible tasks    | Required       |
| GET    | `/tasks/{task_id}` | Get a task by ID        | Required       |
| PATCH  | `/tasks/{task_id}` | Partially update a task | Required       |
| DELETE | `/tasks/{task_id}` | Delete a task           | Required       |

**Create task request:**

```json
{
  "title": "Study FastAPI",
  "description": "Complete the assignment",
  "category_id": 1
}
```

The task owner is determined from the authenticated user. Clients cannot assign tasks to another user.

### Categories

| Method | Endpoint                          | Description             | Authentication |
| ------ | --------------------------------- | ----------------------- | -------------- |
| POST   | `/categories`                     | Create a category       | Public         |
| GET    | `/categories`                     | Get all categories      | Public         |
| GET    | `/categories/{category_id}`       | Get a category          | Public         |
| PUT    | `/categories/{category_id}`       | Update a category       | Public         |
| DELETE | `/categories/{category_id}`       | Delete a category       | Public         |
| GET    | `/categories/{category_id}/tasks` | Get tasks in a category | Public         |

A task can exist without a category. Setting `category_id` to `null` removes its category association without deleting the task.

### Admin

| Method | Endpoint       | Description        | Authentication |
| ------ | -------------- | ------------------ | -------------- |
| GET    | `/admin/tasks` | Retrieve all tasks | Admin only     |

Normal users receive `403 Forbidden` when attempting to access admin-only functionality.

## Data Models

### User

| Field           | Type    | Description     |
| --------------- | ------- | --------------- |
| id              | Integer | Primary key     |
| username        | String  | Unique username |
| hashed_password | String  | Hashed password |
| role            | String  | User role       |

### Task

| Field       | Type           | Description          |
| ----------- | -------------- | -------------------- |
| id          | Integer        | Primary key          |
| title       | String         | Required task title  |
| description | String         | Task description     |
| completed   | Boolean        | Completion status    |
| category_id | Integer / null | Category foreign key |
| owner_id    | Integer        | User foreign key     |

### Category

| Field       | Type          | Description          |
| ----------- | ------------- | -------------------- |
| id          | Integer       | Primary key          |
| name        | String        | Unique category name |
| description | String / null | Category description |

## HTTP Status Codes

| Status | Meaning                             |
| ------ | ----------------------------------- |
| 200    | Successful request                  |
| 201    | Resource created                    |
| 204    | Successful deletion, if applicable  |
| 400    | Invalid request or related resource |
| 401    | Missing or invalid authentication   |
| 403    | Insufficient permissions            |
| 404    | Resource not found                  |
| 422    | Request validation error            |

## Database Migrations

Alembic is used to manage database schema changes.

Apply migrations using:

```bash
alembic upgrade head
```

Check whether model changes require a migration:

```bash
alembic check
```
