from __future__ import annotations

import logging
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import CrystalTransaction
from bot.database.repositories import CrystalTransactionRepository, UserRepository

logger = logging.getLogger(__name__)


class CrystalService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.ct_repo = CrystalTransactionRepository(session)

    async def add_crystals(self, telegram_id: int, amount: int, reason: str) -> int:
        async with self.session.begin_nested():
            new_balance = await self.user_repo.add_crystals(telegram_id, amount)
            await self.ct_repo.create(
                user_id=telegram_id,
                amount=amount,
                reason=reason,
                balance_after=new_balance,
            )
        await self.session.commit()
        logger.info(f"Added {amount} crystals to {telegram_id}. Balance: {new_balance}")
        return new_balance

    async def spend_crystals(self, telegram_id: int, amount: int, reason: str) -> Optional[int]:
        async with self.session.begin_nested():
            new_balance = await self.user_repo.spend_crystals(telegram_id, amount)
            if new_balance is None:
                return None
            await self.ct_repo.create(
                user_id=telegram_id,
                amount=-amount,
                reason=reason,
                balance_after=new_balance,
            )
        await self.session.commit()
        logger.info(f"Spent {amount} crystals from {telegram_id}. Balance: {new_balance}")
        return new_balance

    async def get_balance(self, telegram_id: int) -> int:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        return user.crystal_balance if user else 0

    async def get_history(self, telegram_id: int, limit: int = 20) -> List[CrystalTransaction]:
        return await self.ct_repo.get_user_history(telegram_id, limit)
