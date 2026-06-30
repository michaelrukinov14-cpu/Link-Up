from __future__ import annotations

import logging
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User
from bot.database.repositories import LikeRepository, UserRepository

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.like_repo = LikeRepository(session)

    async def get_next_candidate(self, viewer: User) -> Optional[User]:
        liked_ids = await self.like_repo.get_liked_ids(viewer.telegram_id)
        excluded = list(liked_ids) + [viewer.telegram_id]
        candidates = await self.user_repo.search_candidates(viewer, excluded_ids=excluded, limit=1)
        return candidates[0] if candidates else None

    async def get_candidates_batch(self, viewer: User, limit: int = 10) -> List[User]:
        liked_ids = await self.like_repo.get_liked_ids(viewer.telegram_id)
        excluded = list(liked_ids) + [viewer.telegram_id]
        return await self.user_repo.search_candidates(viewer, excluded_ids=excluded, limit=limit)
