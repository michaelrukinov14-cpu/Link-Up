from __future__ import annotations

import logging
from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User
from bot.database.repositories import BanRepository, UserRepository

logger = logging.getLogger(__name__)


class AdminService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.ban_repo = BanRepository(session)

    async def get_stats(self) -> dict:
        total = await self.user_repo.count_all()
        active = await self.user_repo.count_active()
        premium = await self.user_repo.count_premium()
        banned = await self.user_repo.count_banned()
        today = await self.user_repo.count_today()
        return {
            "total": total,
            "active": active,
            "premium": premium,
            "banned": banned,
            "today": today,
        }

    async def find_users(self, query: str) -> List[User]:
        return await self.user_repo.find_users_by_name_or_id(query)

    async def ban_user(self, telegram_id: int, admin_id: int, reason: Optional[str] = None) -> bool:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False
        async with self.session.begin_nested():
            await self.user_repo.ban(telegram_id)
            await self.ban_repo.create(telegram_id, admin_id, reason)
        await self.session.commit()
        logger.info(f"User {telegram_id} banned by admin {admin_id}")
        return True

    async def unban_user(self, telegram_id: int, admin_id: int) -> bool:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False
        async with self.session.begin_nested():
            await self.user_repo.unban(telegram_id)
            await self.ban_repo.deactivate(telegram_id)
        await self.session.commit()
        logger.info(f"User {telegram_id} unbanned by admin {admin_id}")
        return True

    async def warn_user(self, telegram_id: int) -> Tuple[int, bool]:
        new_count = await self.user_repo.add_warn(telegram_id)
        await self.session.commit()
        auto_banned = new_count >= 3
        logger.info(f"User {telegram_id} warned. Count: {new_count}. Auto-banned: {auto_banned}")
        return new_count, auto_banned

    async def remove_warn(self, telegram_id: int) -> int:
        new_count = await self.user_repo.remove_warn(telegram_id)
        await self.session.commit()
        return new_count

    async def delete_profile(self, telegram_id: int) -> bool:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False
        async with self.session.begin_nested():
            await self.user_repo.deactivate(telegram_id)
        await self.session.commit()
        logger.info(f"Profile of {telegram_id} deleted by admin")
        return True
