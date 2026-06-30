from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.repositories import ReferralRepository, UserRepository
from bot.services.crystal_service import CrystalService

logger = logging.getLogger(__name__)

REFERRAL_BONUS_CRYSTALS = 5


class ReferralService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.referral_repo = ReferralRepository(session)
        self.user_repo = UserRepository(session)
        self.crystal_service = CrystalService(session)

    async def process_referral(self, referrer_id: int, referee_id: int) -> bool:
        existing = await self.referral_repo.get_by_referee(referee_id)
        if existing:
            return False

        async with self.session.begin_nested():
            referral = await self.referral_repo.create(referrer_id, referee_id)

        new_balance = await self.crystal_service.add_crystals(
            referrer_id, REFERRAL_BONUS_CRYSTALS, f"Referral bonus for user {referee_id}"
        )

        async with self.session.begin_nested():
            await self.referral_repo.mark_bonus_given(referral.id, REFERRAL_BONUS_CRYSTALS)

        logger.info(f"Referral processed: {referrer_id} -> {referee_id}, bonus={REFERRAL_BONUS_CRYSTALS}")
        return True

    async def get_referral_count(self, referrer_id: int) -> int:
        return await self.referral_repo.count_by_referrer(referrer_id)

    async def get_referral_code(self, telegram_id: int) -> Optional[str]:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        return user.referral_code if user else None

    async def get_referrer_id(self, telegram_id: int) -> Optional[int]:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        return user.referred_by if user else None
