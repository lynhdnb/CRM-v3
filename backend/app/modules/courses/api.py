"""Course API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.users.models import User
from .crud import (
    create_course,
    get_course_by_id,
    get_courses_by_organizer,
    update_course,
    delete_course,
)
from .models import Course
from .schemas import CourseCreate, CourseResponse, CourseUpdate

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_new_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new course for the current user"""
    return await create_course(db, course_create=course_data, organizer_id=current_user.id)

@router.get("/", response_model=list[CourseResponse])
async def read_my_courses(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of courses created by the current user"""
    return await get_courses_by_organizer(db, organizer_id=current_user.id, skip=skip, limit=limit)

@router.get("/{course_id}", response_model=CourseResponse)
async def read_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific course by ID (must be owned by current user)"""
    course = await get_course_by_id(db, course_id=course_id, organizer_id=current_user.id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course_endpoint(
    course_id: str,
    course_update: CourseUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a specific course (must be owned by current user)"""
    db_course = await get_course_by_id(db, course_id=course_id, organizer_id=current_user.id)
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return await update_course(db, db_course=db_course, course_update=course_update)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course_endpoint(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a specific course (must be owned by current user)"""
    db_course = await get_course_by_id(db, course_id=course_id, organizer_id=current_user.id)
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    await delete_course(db, db_course=db_course)
    return None