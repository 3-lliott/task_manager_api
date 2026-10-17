
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = {
    1: {
        "id": 1,
        "title": "Learn Python",
        "description": "Learn Python with FreeCodeCamp",
        "completed": False
    },
    2: {
        "id": 2,
        "title": "Wash Clothes",
        "description": "Put the clothes in the washing machine",
        "completed": False
    }
}


# Model for data received from the client
class Task(BaseModel):
    title: str
    description: str = ""
    completed: bool = False


# Model for data returned by the API
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str = ""
    completed: bool = False


# Get all tasks
@app.get("/api/v1/tasks", response_model=list[TaskResponse])
def get_all_tasks():
    return list(tasks.values())


# Get a task by ID
@app.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
def get_by_id(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks[task_id]


# Create a task
@app.post(
    "/api/v1/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(task: Task):
    if not task.title.strip():
        raise HTTPException(
            status_code=422,
            detail="Title cannot be empty"
        )

    task_id = max(tasks.keys(), default=0) + 1

    tasks[task_id] = {
        "id": task_id,
        **task.model_dump()
    }

    return tasks[task_id]


# Update a task (PUT replaces the entire task)
@app.put(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=200
)
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if not task.title.strip():
        raise HTTPException(
            status_code=422,
            detail="Title cannot be empty"
        )

    tasks[task_id] = {
        "id": task_id,
        **task.model_dump()
    }

    return tasks[task_id]


# Delete a task
@app.delete(
    "/api/v1/tasks/{task_id}",
    status_code=200
)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    del tasks[task_id]

    return {"message": "Deleted successfully"}
