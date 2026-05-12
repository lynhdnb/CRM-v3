"""Organization API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.users.models import User
from .crud import (
    get_organization_by_id,
    get_organization_by_slug,
    get_organizations,
    update_organization,
    delete_organization,
)
from .models import Organization, user_organization, OrganizationRole
from .schemas import OrganizationCreate, OrganizationResponse, OrganizationUpdate

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_new_org(
    org_data: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create organization + link user as OWNER in one atomic transaction"""
    # Проверка уникальности slug
    existing = await get_organization_by_slug(db, org_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    
    # 1. Создаём организацию
    org = Organization(**org_data.model_dump())
    db.add(org)
    
    # 2. Flush (не commit!) — чтобы сгенерировался org.id для связи
    await db.flush()
    
    # 3. Добавляем связь пользователя с организацией
    # role.value возвращает "owner" (lowercase), что совпадает с CheckConstraint в БД
    stmt = insert(user_organization).values(
        user_id=current_user.id,
        organization_id=org.id,
        role=OrganizationRole.OWNER.value,
        is_active=True
    )
    await db.execute(stmt)
    
    # 4. Один коммит для обеих операций — атомарность
    await db.commit()
    await db.refresh(org)
    
    return org


@router.get("/", response_model=list[OrganizationResponse])
async def read_orgs(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get list of all organizations"""
    return await get_organizations(db, skip=skip, limit=limit)


@router.get("/{org_id}", response_model=OrganizationResponse)
async def read_org(
    org_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific organization by ID"""
    org = await get_organization_by_id(db, org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return org


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_org_endpoint(
    org_id: str,
    org_update: OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update organization details"""
    org = await get_organization_by_id(db, org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return await update_organization(db, db_org=org, org_update=org_update)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_org_endpoint(
    org_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Soft delete an organization"""
    org = await get_organization_by_id(db, org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    await delete_organization(db, db_org=org)
    return None