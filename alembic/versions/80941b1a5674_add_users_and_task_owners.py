
"""add users and task owners

Revision ID: 80941b1a5674
Revises: 001
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "80941b1a5674"
down_revision: Union[str, Sequence[str], None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create users and associate tasks with their owners."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_users_id",
        "users",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_users_username",
        "users",
        ["username"],
        unique=True
    )

    # SQLite requires batch mode to add the foreign key.
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(
            sa.Column("owner_id", sa.Integer(), nullable=False)
        )

        batch_op.create_foreign_key(
            "fk_tasks_owner_id_users",
            "users",
            ["owner_id"],
            ["id"]
        )


def downgrade() -> None:
    """Remove task ownership and users."""

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_constraint(
            "fk_tasks_owner_id_users",
            type_="foreignkey"
        )

        batch_op.drop_column("owner_id")

    op.drop_index(
        "ix_users_username",
        table_name="users"
    )

    op.drop_index(
        "ix_users_id",
        table_name="users"
    )

    op.drop_table("users")
