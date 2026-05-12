"""Course model definition"""
from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.core.models import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=0)
    
    # Привязка к организации и конкретному пользователю-организатору
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    organizer_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    organizer = relationship("User", back_populates="courses")
    organization = relationship("Organization", back_populates="courses")
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self) -> str:
        return f"<Course(id='{self.id}', title='{self.title}', organization_id='{self.organization_id}')>"