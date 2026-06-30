from __future__ import annotations

from typing import List, Optional, Set

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Like, Match


class LikeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_like(self, from_id: int, to_id: int) -> Optional[Like]:
        result = await self.session.execute(
            select(Like).where(Like.from_user_id == from_id, Like.to_user_id == to_id)
        )
        return result.scalar_one_or_none()

    async def add_like(self, from_id: int, to_id: int) -> Like:
        like = Like(from_user_id=from_id, to_user_id=to_id)
        self.session.add(like)
        await self.session.flush()
        return like

    async def check_mutual(self, user1: int, user2: int) -> bool:
        result = await self.session.execute(
            select(Like).where(Like.from_user_id == user2, Like.to_user_id == user1)
        )
        reverse_like = result.scalar_one_or_none()
        return reverse_like is not None

    async def set_mutual(self, from_id: int, to_id: int) -> None:
        await self.session.execute(
            update(Like).where(
                and_(
                    Like.from_user_id.in_([from_id, to_id]),
                    Like.to_user_id.in_([from_id, to_id]),
                )
            ).values(is_mutual=True)
        )
        await self.session.flush()

    async def get_liked_ids(self, telegram_id: int) -> Set[int]:
        result = await self.session.execute(
            select(Like.to_user_id).where(Like.from_user_id == telegram_id)
        )
        return set(result.scalars().all())

    async def get_or_create_match(self, user1_id: int, user2_id: int) -> Match:
        uid1, uid2 = sorted([user1_id, user2_id])
        result = await self.session.execute(
            select(Match).where(Match.user1_id == uid1, Match.user2_id == uid2)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing
        match = Match(user1_id=uid1, user2_id=uid2)
        self.session.add(match)
        await self.session.flush()
        return match

    async def get_matches_for_user(self, telegram_id: int) -> List[Match]:
        result = await self.session.execute(
            select(Match).where(
                (Match.user1_id == telegram_id) | (Match.user2_id == telegram_id)
            )
        )
        return list(result.scalars().all())
