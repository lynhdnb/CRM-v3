"""Pydantic schemas for Course model"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    organization_id: str
    # organizer_id не нужен в запросе — он берётся из токена пользователя

class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None

class CourseResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    organization_id: str
    organizer_id: str
    price: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}