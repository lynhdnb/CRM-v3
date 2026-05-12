"""fix organization role type

Revision ID: fix_role_v1
Revises: add_organizations_v1
Create Date: 2026-05-12 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "fix_role_v1"
down_revision = "add_organizations_v1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Удаляем старую таблицу с ENUM (данные в user_organization пока пустые)
    op.drop_table("user_organization")
    
    # 2. Создаём заново, но role как String с проверкой допустимых значений
    op.create_table(
        "user_organization",
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("organization_id", sa.String(), sa.ForeignKey("organizations.id"), primary_key=True),
        sa.Column("role", sa.String(50), nullable=False, server_default="student"),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        # Проверка на уровне БД: только допустимые роли
        sa.CheckConstraint("role IN ('owner', 'manager', 'teacher', 'student')", name="check_valid_role"),
    )


def downgrade() -> None:
    op.drop_table("user_organization")
    # В downgrade можно воссоздать с Enum, но это сложнее и не нужно сейчас
    op.create_table(
        "user_organization",
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("organization_id", sa.String(), sa.ForeignKey("organizations.id"), primary_key=True),
        sa.Column("role", sa.Enum("owner", "manager", "teacher", "student", name="organizationrole"), nullable=False, server_default=sa.text("'student'")),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
    )