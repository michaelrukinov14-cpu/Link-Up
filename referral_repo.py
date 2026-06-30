from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Referral


class ReferralRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, referrer_id: int, referee_id: int) -> Referral:
        ref = Referral(referrer_id=referrer_id, referee_id=referee_id, bonus_given=False, crystals_awarded=0)
        self.session.add(ref)
        await self.session.flush()
        return ref

    async def get_by_referee(self, referee_id: int) -> Optional[Referral]:
        result = await self.session.execute(
            select(Referral).where(Referral.referee_id == referee_id)
        )
        return result.scalar_one_or_none()

    async def get_by_referrer(self, referrer_id: int) -> List[Referral]:
        result = await self.session.execute(
            select(Referral).where(Referral.referrer_id == referrer_id).order_by(Referral.created_at.desc())
        )
        return list(result.scalars().all())

    async def mark_bonus_given(self, referral_id: int, crystals: int) -> None:
        ref = await self.session.get(Referral, referral_id)
        if ref:
            ref.bonus_given = True
            ref.crystals_awarded = crystals
            await self.session.flush()

    async def count_by_referrer(self, referrer_id: int) -> int:
        refs = await self.get_by_referrer(referrer_id)
        return len(refs)
