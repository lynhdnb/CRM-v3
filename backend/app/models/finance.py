from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
from enum import Enum


class TransactionType(str, Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    EXPENSE = "expense"
    SALARY = "salary"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    payment_date = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="transactions")
    student = relationship("Student")

    def __repr__(self):
        return f"<Transaction {self.id} - {self.amount}>"
