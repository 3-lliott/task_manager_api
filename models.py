
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="category"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default="", nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    category: Mapped["Category | None"] = relationship(
        back_populates="tasks"
    )
