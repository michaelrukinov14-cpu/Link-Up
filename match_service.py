from __future__ import annotations

import logging
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Like, Match, User
from bot.database.repositories import LikeRepository, UserRepository

logger = logging.getLogger(__name__)


class MatchService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.like_repo = LikeRepository(session)
        self.user_repo = UserRepository(session)

    async def process_like(self, from_id: int, to_id: int) -> Tuple[Like, Optional[Match]]:
        existing = await self.like_repo.get_like(from_id, to_id)
        if existing:
            return existing, None

        async with self.session.begin_nested():
            like = await self.like_repo.add_like(from_id, to_id)
            is_mutual = await self.like_repo.check_mutual(from_id, to_id)
            match: Optional[Match] = None
            if is_mutual:
                await self.like_repo.set_mutual(from_id, to_id)
                match = await self.like_repo.get_or_create_match(from_id, to_id)

        await self.session.commit()
        logger.info(f"Like from {from_id} to {to_id}. Mutual: {is_mutual}")
        return like, match

    async def get_matches_for_user(self, telegram_id: int):
        return await self.like_repo.get_matches_for_user(telegram_id)

    async def get_liked_ids(self, telegram_id: int):
        return await self.like_repo.get_liked_ids(telegram_id)
