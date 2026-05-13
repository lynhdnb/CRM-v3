"""Course API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.users.models import User
from app.modules.organizations.models import user_organization
from .crud import (
    create_course,
    get_course_by_id,
    get_courses,
    update_course,
    delete_course,
)
from .schemas import CourseCreate, CourseResponse, CourseUpdate

router = APIRouter(prefix="/courses", tags=["courses"])


async def verify_org_access(db: AsyncSession, user: User, org_id: str) -> str:
    """Проверяет, что пользователь состоит в организации и она активна"""
    result = await db.execute(
        select(user_organization).where(
            user_organization.c.user_id == user.id,
            user_organization.c.organization_id == org_id,
            user_organization.c.is_active == True
        )
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой организации"
        )
    return org_id


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_new_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_user),
    x_organization_id: str | None = Header(None, alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Создать курс в контексте организации"""
    target_org_id = x_organization_id or course_data.organization_id
    if not target_org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется указать организацию"
        )
    
    await verify_org_access(db, current_user, target_org_id)
    course_data.organization_id = target_org_id
    
    # 🔧 Исправлено: передаём organizer_id из токена пользователя
    return await create_course(db, course_data=course_data, organizer_id=current_user.id)


@router.get("/", response_model=list[CourseResponse])
async def read_courses(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    x_organization_id: str | None = Header(None, alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Список курсов с фильтрацией по организации"""
    if x_organization_id:
        await verify_org_access(db, current_user, x_organization_id)
        
    return await get_courses(db, organization_id=x_organization_id, skip=skip, limit=limit)


@router.get("/{course_id}", response_model=CourseResponse)
async def read_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    x_organization_id: str | None = Header(None, alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Получить курс по ID"""
    course = await get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
    if x_organization_id and course.organization_id != x_organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Курс не принадлежит выбранной организации"
        )
        
    await verify_org_access(db, current_user, course.organization_id)
    return course


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course_endpoint(
    course_id: str,
    course_update: CourseUpdate,
    current_user: User = Depends(get_current_user),
    x_organization_id: str | None = Header(None, alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Обновить курс"""
    course = await get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
    target_org = x_organization_id or course.organization_id
    await verify_org_access(db, current_user, target_org)
    return await update_course(db, db_course=course, course_update=course_update)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course_endpoint(
    course_id: str,
    current_user: User = Depends(get_current_user),
    x_organization_id: str | None = Header(None, alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Удалить курс"""
    course = await get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
    target_org = x_organization_id or course.organization_id
    await verify_org_access(db, current_user, target_org)
    await delete_course(db, db_course=course)
    return None