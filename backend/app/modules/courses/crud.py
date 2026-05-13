"""CRUD operations for Course model"""
from typing import Sequence, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Course
from .schemas import CourseCreate, CourseUpdate


async def create_course(
    session: AsyncSession,
    course_data: CourseCreate,
    organizer_id: str
) -> Course:
    """Create a new course"""
    db_course = Course(
        title=course_data.title,
        description=course_data.description,
        organization_id=course_data.organization_id,
        organizer_id=organizer_id,
        price=0  # Default price if not provided
    )
    session.add(db_course)
    await session.commit()
    await session.refresh(db_course)
    return db_course


async def get_course_by_id(session: AsyncSession, course_id: str) -> Optional[Course]:
    """Get course by ID"""
    result = await session.execute(
        select(Course)
        .where(Course.id == course_id)
        .options(selectinload(Course.organization))
    )
    return result.scalar_one_or_none()


async def get_courses(
    session: AsyncSession,
    organization_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
) -> Sequence[Course]:
    """Get list of courses with optional organization filter"""
    stmt = select(Course)
    
    if organization_id:
        stmt = stmt.where(Course.organization_id == organization_id)
    
    stmt = stmt.offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_course(
    session: AsyncSession,
    db_course: Course,
    course_update: CourseUpdate
) -> Course:
    """Update course fields"""
    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    session.add(db_course)
    await session.commit()
    await session.refresh(db_course)
    return db_course


async def delete_course(session: AsyncSession, db_course: Course) -> None:
    """Soft delete: mark course as inactive"""
    db_course.is_active = False
    session.add(db_course)
    await session.commit()