from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Premium, PremiumPlanEnum


class PremiumRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        user_id: int,
        plan: PremiumPlanEnum,
        expires_at: datetime,
        payment_method: str,
    ) -> Premium:
        await self.session.execute(
            update(Premium).where(Premium.user_id == user_id, Premium.is_active == True).values(is_active=False)
        )
        premium = Premium(
            user_id=user_id,
            plan=plan,
            expires_at=expires_at,
            payment_method=payment_method,
            is_active=True,
        )
        self.session.add(premium)
        await self.session.flush()
        return premium

    async def get_active(self, user_id: int) -> Optional[Premium]:
        result = await self.session.execute(
            select(Premium).where(Premium.user_id == user_id, Premium.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_history(self, user_id: int) -> List[Premium]:
        result = await self.session.execute(
            select(Premium).where(Premium.user_id == user_id).order_by(Premium.started_at.desc())
        )
        return list(result.scalars().all())

    async def deactivate_expired(self) -> List[int]:
        now = datetime.now()
        result = await self.session.execute(
            select(Premium).where(Premium.is_active == True, Premium.expires_at <= now)
        )
        expired = list(result.scalars().all())
        ids = []
        for p in expired:
            p.is_active = False
            ids.append(p.user_id)
        await self.session.flush()
        return ids
