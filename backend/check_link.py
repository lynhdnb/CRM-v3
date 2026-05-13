"""Script to check user_organization link in DB"""
import asyncio
from sqlalchemy import text
from app.core.database import async_session

async def check_link():
    user_id = "b12a28e0-adb1-4283-9441-188461bf824e"  # ID из твоего токена
    org_id = "ed009eca-16bc-45f5-a3df-2d6c6ea22a53"    # ID "Импульс"
    
    async with async_session() as session:
        # Прямой SQL-запрос
        result = await session.execute(
            text("SELECT user_id, organization_id, role, is_active FROM user_organization WHERE user_id = :uid AND organization_id = :oid"),
            {"uid": user_id, "oid": org_id}
        )
        row = result.first()
        if row:
            print(f"✅ Запись найдена: role={row.role}, is_active={row.is_active}")
        else:
            print("❌ Запись НЕ найдена. Пользователь не состоит в организации.")
            
        # Покажем все связи этого пользователя
        all_links = await session.execute(
            text("SELECT organization_id, role, is_active FROM user_organization WHERE user_id = :uid"),
            {"uid": user_id}
        )
        links = all_links.all()
        if links:
            print(f"\n📋 Все связи пользователя {user_id}:")
            for l in links:
                print(f"   Org: {l.organization_id}, Role: {l.role}, Active: {l.is_active}")
        else:
            print(f"\n📋 У пользователя нет НИ ОДНОЙ связи с организациями.")

if __name__ == "__main__":
    asyncio.run(check_link())