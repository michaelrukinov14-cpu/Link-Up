from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.repositories import UserRepository
from bot.locales import detect_language

logger = logging.getLogger(__name__)


class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        telegram_user = data.get("event_from_user")
        session: AsyncSession = data.get("session")

        lang = "ru"
        user_db = None

        if telegram_user and session:
            user_repo = UserRepository(session)
            user_db = await user_repo.get_by_telegram_id(telegram_user.id)
            if user_db:
                lang = user_db.language
            else:
                lang = detect_language(telegram_user.language_code or "ru")

        data["lang"] = lang
        data["user_db"] = user_db

        return await handler(event, data)
