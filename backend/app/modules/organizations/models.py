"""Organization model definition"""
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, ForeignKey, Table, Numeric, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
import enum

from app.core.models import Base


class OrganizationRole(str, enum.Enum):
    """Роли пользователя в контексте организации (Python-валидация)"""
    OWNER = "owner"
    MANAGER = "manager"
    TEACHER = "teacher"
    STUDENT = "student"


# Таблица-связка: пользователи ↔ организации
# role хранится как String с проверкой допустимых значений на уровне БД
user_organization = Table(
    "user_organization",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("organization_id", String, ForeignKey("organizations.id"), primary_key=True),
    Column("role", String(50), nullable=False, server_default="student"),  # ← String, не Enum!
    Column("joined_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    # Проверка на уровне БД: только допустимые роли (нижний регистр)
    CheckConstraint("role IN ('owner', 'manager', 'teacher', 'student')", name="check_valid_role"),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    short_name = Column(String(100), nullable=True)
    
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), default="Russia", nullable=False)
    timezone = Column(String(50), default="Asia/Yekaterinburg", nullable=False)
    
    currency = Column(String(3), default="RUB", nullable=False)
    language = Column(String(10), default="ru", nullable=False)
    commission_rate = Column(Numeric(5, 4), default=0.0, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    users = relationship(
        "User",
        secondary=user_organization,
        back_populates="organizations",
        lazy="select"
    )
    courses = relationship("Course", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Organization(id='{self.id}', slug='{self.slug}', name='{self.name}')>"