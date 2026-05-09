from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    inn = Column(String(12), unique=True)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    members = relationship("OrganizationMember", back_populates="organization")
    courses = relationship("Course", back_populates="organization")
    groups = relationship("Group", back_populates="organization")
    rooms = relationship("Room", back_populates="organization")
    transactions = relationship("Transaction", back_populates="organization")

    def __repr__(self):
        return f"<Organization {self.name}>"


class OrganizationMember(Base):
    __tablename__ = "organization_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # admin, teacher, student, parent
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="organizations")
    organization = relationship("Organization", back_populates="members")
