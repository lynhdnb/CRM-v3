from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    inn: Optional[str] = Field(None, max_length=12)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    inn: Optional[str] = Field(None, max_length=12)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class OrganizationResponse(OrganizationBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    duration_months: Optional[int] = Field(None, gt=0)


class CourseCreate(CourseBase):
    organization_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    duration_months: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class CourseResponse(CourseBase):
    id: int
    organization_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    start_date: date
    end_date: Optional[date] = None
    max_students: int = Field(default=15, gt=0)


class GroupCreate(GroupBase):
    organization_id: int
    course_id: int


class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    end_date: Optional[date] = None
    max_students: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class GroupResponse(GroupBase):
    id: int
    organization_id: int
    course_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
