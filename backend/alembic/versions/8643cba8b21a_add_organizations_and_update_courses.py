"""add organizations and update courses

Revision ID: add_organizations_v1
Revises: courses_v1
Create Date: 2026-05-12 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "add_organizations_v1"
down_revision = "courses_v1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Создаём таблицу организаций
    op.create_table(
        "organizations",
        sa.Column("id", sa.String(), primary_key=True, index=True),
        sa.Column("slug", sa.String(100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("short_name", sa.String(100), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("website", sa.String(255), nullable=True),
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("country", sa.String(100), server_default=sa.text("'Russia'"), nullable=False),
        sa.Column("timezone", sa.String(50), server_default=sa.text("'Asia/Yekaterinburg'"), nullable=False),
        sa.Column("currency", sa.String(3), server_default=sa.text("'RUB'"), nullable=False),
        sa.Column("language", sa.String(10), server_default=sa.text("'ru'"), nullable=False),
        sa.Column("commission_rate", sa.Numeric(5, 4), server_default=sa.text("0.0"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("is_verified", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now(), nullable=True),
    )

    # 2. Создаём таблицу-связку пользователей и организаций
    op.create_table(
        "user_organization",
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("organization_id", sa.String(), sa.ForeignKey("organizations.id"), primary_key=True),
        sa.Column("role", sa.Enum("owner", "manager", "teacher", "student", name="organizationrole"), nullable=False, server_default=sa.text("'student'")),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
    )

    # 3. Добавляем organization_id в курсы (nullable=True для обратной совместимости)
    op.add_column("courses", sa.Column("organization_id", sa.String(), sa.ForeignKey("organizations.id"), nullable=True))
    op.create_index("ix_courses_organization_id", "courses", ["organization_id"])


def downgrade() -> None:
    op.drop_index("ix_courses_organization_id", table_name="courses")
    op.drop_column("courses", "organization_id")
    op.drop_table("user_organization")
    op.drop_table("organizations")