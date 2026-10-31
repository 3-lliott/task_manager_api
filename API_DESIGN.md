# Task Manager API Design

Base URL: `/api/v1`

## Categories

| Method | Endpoint                        | Description             |
| ------ | ------------------------------- | ----------------------- |
| POST   | /categories                     | Create a category       |
| GET    | /categories                     | Get all categories      |
| GET    | /categories/{category_id}       | Get a category          |
| PUT    | /categories/{category_id}       | Update a category       |
| DELETE | /categories/{category_id}       | Delete a category       |
| GET    | /categories/{category_id}/tasks | Get tasks in a category |

## Tasks

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| POST   | /tasks           | Create a task           |
| GET    | /tasks           | Get all tasks           |
| GET    | /tasks/{task_id} | Get a task              |
| PATCH  | /tasks/{task_id} | Partially update a task |
| DELETE | /tasks/{task_id} | Delete a task           |

## Task Fields

- id: Automatically generated integer.
- title: Required string.
- description: Optional string.
- completed: Boolean, defaults to false.
- category_id: Optional foreign key referencing categories.id.

## Category Fields

- id: Automatically generated integer.
- name: Required unique string.
- description: Optional string.

## Relationships

One category can have many tasks.

A task can belong to one category or no category.

Deleting a category removes its association from its tasks.
The tasks themselves are not deleted.

## Validation and Error Handling

- 201: Resource successfully created.
- 200: Successful retrieval or update.
- 200: Successful deletion.
- 400: Invalid category ID or duplicate category name.
- 404: Requested task or category does not exist.
- 422: Invalid request body.
