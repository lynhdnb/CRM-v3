"""Pydantic schemas for Course model"""
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CourseCreate(BaseModel):
    """Схема для создания курса"""
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(default=0.00, ge=0)


class CourseUpdate(BaseModel):
    """Схема для обновления курса"""
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None


class CourseResponse(BaseModel):
    """Схема ответа с данными курса"""
    model_config = {"from_attributes": True}
    
    id: str
    title: str
    description: Optional[str] = None
    price: Decimal
    organizer_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None