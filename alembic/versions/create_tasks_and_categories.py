
from alembic import op
import sqlalchemy as sa


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create categories table
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
    )

    op.create_index(
        "ix_categories_id",
        "categories",
        ["id"]
    )

    op.create_index(
        "ix_categories_name",
        "categories",
        ["name"],
        unique=True
    )

    # Create tasks table
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("category_id", sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"]
        )
    )

    op.create_index(
        "ix_tasks_id",
        "tasks",
        ["id"]
    )


def downgrade():
    op.drop_index("ix_tasks_id", table_name="tasks")
    op.drop_table("tasks")

    op.drop_index("ix_categories_name", table_name="categories")
    op.drop_index("ix_categories_id", table_name="categories")
    op.drop_table("categories")
