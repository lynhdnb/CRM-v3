"""CRUD operations for Organization model"""
from typing import Sequence
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Organization, user_organization, OrganizationRole
from .schemas import OrganizationCreate, OrganizationUpdate


async def create_organization(session: AsyncSession, org_data: OrganizationCreate) -> Organization:
    """Create a new organization"""
    db_org = Organization(**org_data.model_dump())
    session.add(db_org)
    await session.commit()
    await session.refresh(db_org)
    return db_org


async def get_organization_by_id(session: AsyncSession, org_id: str) -> Organization | None:
    """Get organization by ID"""
    result = await session.execute(select(Organization).where(Organization.id == org_id))
    return result.scalar_one_or_none()


async def get_organization_by_slug(session: AsyncSession, slug: str) -> Organization | None:
    """Get organization by URL slug"""
    result = await session.execute(select(Organization).where(Organization.slug == slug))
    return result.scalar_one_or_none()


async def get_organizations(session: AsyncSession, skip: int = 0, limit: int = 10) -> Sequence[Organization]:
    """Get list of organizations with pagination"""
    result = await session.execute(select(Organization).offset(skip).limit(limit))
    return result.scalars().all()


async def add_user_to_org(
    session: AsyncSession,
    user_id: str,
    org_id: str,
    role: OrganizationRole = OrganizationRole.STUDENT
) -> None:
    """Link a user to an organization with a specific role"""
    # Передаём .value (lowercase), что совпадает с CheckConstraint в БД
    stmt = insert(user_organization).values(
        user_id=user_id,
        organization_id=org_id,
        role=role.value,  # "owner", "manager", etc.
        is_active=True
    )
    await session.execute(stmt)
    await session.commit()


async def update_organization(
    session: AsyncSession,
    db_org: Organization,
    org_update: OrganizationUpdate
) -> Organization:
    """Update organization fields"""
    update_data = org_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_org, key, value)
    
    session.add(db_org)
    await session.commit()
    await session.refresh(db_org)
    return db_org


async def delete_organization(session: AsyncSession, db_org: Organization) -> bool:
    """Soft delete: mark organization as inactive"""
    db_org.is_active = False
    session.add(db_org)
    await session.commit()
    return True