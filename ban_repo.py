from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Ban


class BanRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int, admin_id: int, reason: Optional[str] = None) -> Ban:
        ban = Ban(user_id=user_id, admin_id=admin_id, reason=reason, is_active=True)
        self.session.add(ban)
        await self.session.flush()
        return ban

    async def deactivate(self, user_id: int) -> None:
        await self.session.execute(
            update(Ban).where(Ban.user_id == user_id, Ban.is_active == True).values(is_active=False)
        )
        await self.session.flush()

    async def get_active(self, user_id: int) -> Optional[Ban]:
        result = await self.session.execute(
            select(Ban).where(Ban.user_id == user_id, Ban.is_active == True).order_by(Ban.created_at.desc())
        )
        return result.scalar_one_or_none()

    async def get_history(self, user_id: int) -> List[Ban]:
        result = await self.session.execute(
            select(Ban).where(Ban.user_id == user_id).order_by(Ban.created_at.desc())
        )
        return list(result.scalars().all())
