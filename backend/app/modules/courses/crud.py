"""CRUD operations for Course model"""
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Course
from .schemas import CourseCreate, CourseUpdate


async def create_course(
    session: AsyncSession,
    course_create: CourseCreate,
    organizer_id: str
) -> Course:
    """Create a new course for a specific user"""
    db_course = Course(
        organizer_id=organizer_id,
        **course_create.model_dump()
    )
    session.add(db_course)
    await session.commit()
    await session.refresh(db_course)
    return db_course


async def get_course_by_id(
    session: AsyncSession,
    course_id: str,
    organizer_id: str
) -> Course | None:
    """Get a course by ID, checking ownership and active status"""
    result = await session.execute(
        select(Course).where(
            Course.id == course_id,
            Course.organizer_id == organizer_id,
            Course.is_active == True  # noqa: E712
        )
    )
    return result.scalar_one_or_none()


async def get_courses_by_organizer(
    session: AsyncSession,
    organizer_id: str,
    skip: int = 0,
    limit: int = 10
) -> Sequence[Course]:
    """Get list of ACTIVE courses for a specific organizer"""
    result = await session.execute(
        select(Course)
        .where(
            Course.organizer_id == organizer_id,
            Course.is_active == True  # noqa: E712
        )
        .offset(skip)
        .limit(limit)
    )
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


async def delete_course(
    session: AsyncSession,
    db_course: Course
) -> bool:
    """Soft delete: mark course as inactive"""
    db_course.is_active = False
    session.add(db_course)
    await session.commit()
    return True