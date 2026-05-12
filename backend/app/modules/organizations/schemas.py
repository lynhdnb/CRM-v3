"""Pydantic schemas for Organization model"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from .models import OrganizationRole


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    slug: str = Field(..., min_length=3, max_length=100, description="URL-friendly identifier (e.g., 'school-name')")
    description: Optional[str] = None
    short_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: str = "Russia"
    timezone: str = "Asia/Yekaterinburg"
    currency: str = "RUB"
    language: str = "ru"


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class OrganizationResponse(OrganizationBase):
    model_config = {"from_attributes": True}
    
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None