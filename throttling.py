from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from redis.asyncio import Redis

from bot.config import config

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, rate: float = 0.5) -> None:
        self.redis = redis
        self.rate = rate
        self.prefix = config.throttle_key_prefix

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        key = f"{self.prefix}{user.id}"
        exists = await self.redis.exists(key)

        if exists:
            if isinstance(event, Message):
                lang = data.get("lang", "ru")
                from bot.locales import get_string
                try:
                    await event.answer(get_string(lang, "throttle_message"))
                except Exception:
                    pass
            return

        await self.redis.set(key, "1", ex=int(self.rate * 1000) if self.rate < 1 else int(self.rate))
        return await handler(event, data)
