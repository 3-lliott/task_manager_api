from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Task, Category
from schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    CategoryCreate,
    CategoryResponse
)

app = FastAPI()


# CATEGORY ENDPOINTS

# Create a category
@app.post(
    "/api/v1/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing_category = db.query(Category).filter(
        Category.name == category.name
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = Category(**category.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# Get all categories
@app.get(
    "/api/v1/categories",
    response_model=list[CategoryResponse]
)
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


# Get a category by ID
@app.get(
    "/api/v1/categories/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


# Update a category
@app.put(
    "/api/v1/categories/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    duplicate = db.query(Category).filter(
        Category.name == category_data.name,
        Category.id != category_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Category name already exists"
        )

    category.name = category_data.name
    category.description = category_data.description

    db.commit()
    db.refresh(category)

    return category


# Delete a category
@app.delete("/api/v1/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    # Remove the category association from its tasks
    for task in category.tasks:
        task.category_id = None

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}


# Get all tasks belonging to a category
@app.get(
    "/api/v1/categories/{category_id}/tasks",
    response_model=list[TaskResponse]
)
def get_category_tasks(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category.tasks



# TASK ENDPOINTS


# Create a task
@app.post(
    "/api/v1/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    if task.category_id is not None:
        category = db.query(Category).filter(
            Category.id == task.category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=400,
                detail="Invalid category ID"
            )

    new_task = Task(**task.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# Get all tasks
@app.get(
    "/api/v1/tasks",
    response_model=list[TaskResponse]
)
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


# Get a task by ID
@app.get(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Update a task
@app.patch(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    updates = task_data.model_dump(exclude_unset=True)

    if "category_id" in updates and updates["category_id"] is not None:
        category = db.query(Category).filter(
            Category.id == updates["category_id"]
        ).first()

        if not category:
            raise HTTPException(
                status_code=400,
                detail="Invalid category ID"
            )

    for key, value in updates.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# Delete a task
@app.delete("/api/v1/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}