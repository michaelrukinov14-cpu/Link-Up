from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import TransactionTypeEnum
from bot.database.repositories import TransactionRepository

logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.tx_repo = TransactionRepository(session)

    async def record_stars_payment(
        self,
        user_id: int,
        amount_stars: int,
        payload: str,
        telegram_payment_charge_id: str,
        provider_payment_charge_id: Optional[str] = None,
    ) -> None:
        async with self.session.begin_nested():
            await self.tx_repo.create(
                user_id=user_id,
                type=TransactionTypeEnum.stars_purchase,
                amount_stars=amount_stars,
                telegram_payment_charge_id=telegram_payment_charge_id,
                provider_payment_charge_id=provider_payment_charge_id,
                payload=payload,
                status="completed",
            )
        await self.session.commit()
        logger.info(f"Stars payment recorded: user={user_id}, amount={amount_stars}, payload={payload}")

    async def record_card_payment(
        self,
        user_id: int,
        amount_fiat: int,
        currency: str,
        payload: str,
        telegram_payment_charge_id: str,
        provider_payment_charge_id: Optional[str] = None,
    ) -> None:
        async with self.session.begin_nested():
            await self.tx_repo.create(
                user_id=user_id,
                type=TransactionTypeEnum.card_purchase,
                amount_fiat=amount_fiat,
                currency=currency,
                telegram_payment_charge_id=telegram_payment_charge_id,
                provider_payment_charge_id=provider_payment_charge_id,
                payload=payload,
                status="completed",
            )
        await self.session.commit()
        logger.info(f"Card payment recorded: user={user_id}, amount={amount_fiat} {currency}")

    async def is_duplicate_payment(self, charge_id: str) -> bool:
        tx = await self.tx_repo.get_by_charge_id(charge_id)
        return tx is not None
