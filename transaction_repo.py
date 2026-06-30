from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import CrystalTransaction, Transaction, TransactionTypeEnum


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        user_id: int,
        type: TransactionTypeEnum,
        amount_stars: Optional[int] = None,
        amount_crystals: Optional[int] = None,
        amount_fiat: Optional[int] = None,
        currency: Optional[str] = None,
        telegram_payment_charge_id: Optional[str] = None,
        provider_payment_charge_id: Optional[str] = None,
        payload: Optional[str] = None,
        status: str = "completed",
    ) -> Transaction:
        tx = Transaction(
            user_id=user_id,
            type=type,
            amount_stars=amount_stars,
            amount_crystals=amount_crystals,
            amount_fiat=amount_fiat,
            currency=currency,
            telegram_payment_charge_id=telegram_payment_charge_id,
            provider_payment_charge_id=provider_payment_charge_id,
            payload=payload,
            status=status,
        )
        self.session.add(tx)
        await self.session.flush()
        return tx

    async def get_user_history(self, user_id: int, limit: int = 20) -> List[Transaction]:
        result = await self.session.execute(
            select(Transaction).where(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_charge_id(self, charge_id: str) -> Optional[Transaction]:
        result = await self.session.execute(
            select(Transaction).where(Transaction.telegram_payment_charge_id == charge_id)
        )
        return result.scalar_one_or_none()


class CrystalTransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int, amount: int, reason: str, balance_after: int) -> CrystalTransaction:
        ct = CrystalTransaction(user_id=user_id, amount=amount, reason=reason, balance_after=balance_after)
        self.session.add(ct)
        await self.session.flush()
        return ct

    async def get_user_history(self, user_id: int, limit: int = 20) -> List[CrystalTransaction]:
        result = await self.session.execute(
            select(CrystalTransaction).where(CrystalTransaction.user_id == user_id)
            .order_by(CrystalTransaction.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
