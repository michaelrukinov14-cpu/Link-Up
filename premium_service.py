from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import PremiumPlanEnum, User
from bot.database.repositories import PremiumRepository, UserRepository

logger = logging.getLogger(__name__)


class PremiumService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.premium_repo = PremiumRepository(session)
        self.user_repo = UserRepository(session)

    def _get_expiry(self, plan: PremiumPlanEnum, from_date: Optional[datetime] = None) -> datetime:
        base = from_date or datetime.now(timezone.utc)
        if plan == PremiumPlanEnum.month:
            return base + timedelta(days=30)
        elif plan == PremiumPlanEnum.year:
            return base + timedelta(days=365)
        return base + timedelta(days=30)

    async def activate_premium(self, user_id: int, plan: PremiumPlanEnum, payment_method: str) -> datetime:
        user = await self.user_repo.get_by_telegram_id(user_id)
        base_date = None
        if user and user.is_premium and user.premium_until:
            now = datetime.now(timezone.utc)
            pu = user.premium_until
            if pu.tzinfo is None:
                pu = pu.replace(tzinfo=timezone.utc)
            if pu > now:
                base_date = pu

        expires_at = self._get_expiry(plan, base_date)

        async with self.session.begin_nested():
            await self.premium_repo.create(
                user_id=user_id,
                plan=plan,
                expires_at=expires_at,
                payment_method=payment_method,
            )
            await self.user_repo.set_premium(user_id, expires_at)

        await self.session.commit()
        logger.info(f"Premium activated for {user_id}, plan={plan}, until={expires_at}")
        return expires_at

    async def check_and_expire_premiums(self) -> None:
        async with self.session.begin_nested():
            expired_ids = await self.premium_repo.deactivate_expired()
            for uid in expired_ids:
                await self.user_repo.expire_premium(uid)
        if expired_ids:
            await self.session.commit()
            logger.info(f"Expired premiums for {len(expired_ids)} users")

    async def is_active(self, user_id: int) -> bool:
        user = await self.user_repo.get_by_telegram_id(user_id)
        if not user or not user.is_premium or not user.premium_until:
            return False
        pu = user.premium_until
        if pu.tzinfo is None:
            pu = pu.replace(tzinfo=timezone.utc)
        return pu > datetime.now(timezone.utc)
