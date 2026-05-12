"""Simple DB connection test via SQLAlchemy"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text  # <-- Добавлено

from app.core.config import settings

async def test():
    try:
        engine = create_async_engine(settings.DATABASE_URL, echo=False)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))  # <-- Исправлено
            print("✅ Connected to database via SQLAlchemy!")
        await engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test())