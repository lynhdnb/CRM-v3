"""User model definition"""
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.core.models import Base
from app.modules.organizations.models import user_organization


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Отношения
    courses = relationship("Course", back_populates="organizer", cascade="all, delete-orphan")
    organizations = relationship(
        "Organization",
        secondary=user_organization,
        back_populates="users"
    )

    def __repr__(self) -> str:
        return f"<User(id='{self.id}', email='{self.email}', is_active={self.is_active})>"