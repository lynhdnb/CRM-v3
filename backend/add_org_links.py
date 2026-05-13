"""Script to manually add missing user_organization links"""
import asyncio
from sqlalchemy import text
from app.core.database import async_session

async def add_links():
    user_id = "b12a28e0-adb1-4283-9441-188461bf824e"
    targets = [
        ("ed009eca-16bc-45f5-a3df-2d6c6ea22a53", "Импульс"),
        ("1176a873-5d2e-4119-ac54-2970ba61fa1a", "Кодо")
    ]
    
    async with async_session() as session:
        for org_id, org_name in targets:
            await session.execute(
                text("""
                    INSERT INTO user_organization (user_id, organization_id, role, is_active)
                    VALUES (:uid, :oid, 'owner', true)
                    ON CONFLICT (user_id, organization_id) DO NOTHING
                """),
                {"uid": user_id, "oid": org_id}
            )
        await session.commit()
        print(f"✅ Связи добавлены. Теперь пользователь имеет доступ к: {', '.join([n for _, n in targets])}")

if __name__ == "__main__":
    asyncio.run(add_links())