"""reset user_organization table - fix role column type

Revision ID: reset_user_org_v1
Revises: fix_role_v1
Create Date: 2026-05-12 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "reset_user_org_v1"
down_revision = "fix_role_v1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Удаляем таблицу с проблемным ENUM
    op.drop_table("user_organization")
    
    # Создаём заново: role как String + CheckConstraint для валидации
    op.create_table(
        "user_organization",
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("organization_id", sa.String(), sa.ForeignKey("organizations.id"), primary_key=True),
        sa.Column("role", sa.String(50), nullable=False, server_default="student"),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        # Проверка на уровне БД: только допустимые роли (нижний регистр)
        sa.CheckConstraint("role IN ('owner', 'manager', 'teacher', 'student')", name="check_valid_role"),
    )
    # Индекс для быстрых запросов по организации
    op.create_index("ix_user_org_org_id", "user_organization", ["organization_id"])
    op.create_index("ix_user_org_user_id", "user_organization", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_user_org_user_id", table_name="user_organization")
    op.drop_index("ix_user_org_org_id", table_name="user_organization")
    op.drop_table("user_organization")