from pydantic import BaseModel, ConfigDict, Field, field_validator


# CATEGORY SCHEMAS

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Category name cannot be empty")

        return value


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)


# TASK SCHEMAS

class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = ""
    category_id: int | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    category_id: int | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    category_id: int | None
    category: CategoryResponse | None = None

    model_config = ConfigDict(from_attributes=True)