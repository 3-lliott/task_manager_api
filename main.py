
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import TaskModel
from schemas import TaskCreate, TaskResponse, TaskUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI()


# Get all tasks
@app.get("/api/v1/tasks", response_model=list[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()


# Get a task by ID
@app.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
def get_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Create a task
@app.post(
    "/api/v1/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    if not task.title.strip():
        raise HTTPException(
            status_code=422,
            detail="Title cannot be empty"
        )

    new_task = TaskModel(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# Update a task (PUT replaces the entire task)
@app.put(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=200
)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    existing_task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task.model_dump(exclude_unset=True)

    if "title" in update_data:
        if (
            update_data["title"] is None
            or not update_data["title"].strip()
        ):
            raise HTTPException(
                status_code=422,
                detail="Title cannot be empty"
            )

    for field, value in update_data.items():
        setattr(existing_task, field, value)

    db.commit()
    db.refresh(existing_task)

    return existing_task



# Delete a task
@app.delete(
    "/api/v1/tasks/{task_id}",
    status_code=200
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Deleted successfully"}
