from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

logger = logging.getLogger(__name__)


class BanCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_data = data.get("user_db")
        if user_data and user_data.is_banned:
            lang = data.get("lang", "ru")
            from bot.locales import get_string
            if isinstance(event, Message):
                try:
                    await event.answer(get_string(lang, "banned_message"))
                except Exception:
                    pass
            return
        return await handler(event, data)
