from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import Task, Category, User

from schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    CategoryCreate,
    CategoryResponse,
    UserCreate,
    UserResponse,
    Token
)

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_admin
)


app = FastAPI()


# AUTHENTICATION ENDPOINTS

# Sign up
@app.post(
    "/api/v1/auth/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login
@app.post(
    "/api/v1/auth/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


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
def get_categories(
    db: Session = Depends(get_db)
):
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

    return {
        "message": "Category deleted successfully"
    }


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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    new_task = Task(
        **task.model_dump(),
        owner_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# Get all tasks
@app.get(
    "/api/v1/tasks",
    response_model=list[TaskResponse]
)
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admins can see all tasks
    if current_user.role == "admin":
        return db.query(Task).all()

    # Normal users can only see their own tasks
    return db.query(Task).filter(
        Task.owner_id == current_user.id
    ).all()


# Get a task by ID
@app.get(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Only the owner or an admin can access the task
    if (
        current_user.role != "admin"
        and task.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this task"
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Only the owner or an admin can update the task
    if (
        current_user.role != "admin"
        and task.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this task"
        )

    updates = task_data.model_dump(
        exclude_unset=True
    )

    if (
        "category_id" in updates
        and updates["category_id"] is not None
    ):
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Only the owner or an admin can delete the task
    if (
        current_user.role != "admin"
        and task.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this task"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }

# ADMIN ENDPOINTS

# Get all tasks as an administrator
@app.get(
    "/api/v1/admin/tasks",
    response_model=list[TaskResponse]
)
def admin_get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Task).all()