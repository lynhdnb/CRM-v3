"""CRUD operations for User model"""
from typing import Sequence, Optional
from uuid import uuid4

from passlib.context import CryptContext
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    """Create a new user in the database"""
    hashed_password = pwd_context.hash(user_create.password)
    db_user = User(
        id=str(uuid4()),
        email=user_create.email,
        hashed_password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Get user by email"""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: str) -> User | None:
    """Get user by ID"""
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession, skip: int = 0, limit: int = 10) -> Sequence[User]:
    """Get list of users with pagination"""
    result = await session.execute(
        select(User).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate
) -> User:
    """Update user fields"""
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Если обновляется пароль — хешируем его
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))
    
    # Обновляем поля
    for field, value in update_data.items():
        if value is not None:
            setattr(user, field, value)
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user: User) -> bool:
    """Soft delete: mark user as inactive"""
    user.is_active = False
    session.add(user)
    await session.commit()
    return True