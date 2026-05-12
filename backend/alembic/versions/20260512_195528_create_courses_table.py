"""create courses table

Revision ID: courses_v1
Revises: 13be091dda2e
Create Date: 2026-05-12 19:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "courses_v1"
down_revision = "13be091dda2e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("id", sa.String(), primary_key=True, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("organizer_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),  # ← убран index=True
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now(), nullable=True),
    )
    op.create_index("ix_courses_organizer_id", "courses", ["organizer_id"])


def downgrade() -> None:
    op.drop_index("ix_courses_organizer_id", table_name="courses")
    op.drop_table("courses")