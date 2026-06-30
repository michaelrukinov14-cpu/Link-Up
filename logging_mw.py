from __future__ import annotations

import logging
import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        start = time.monotonic()
        user = data.get("event_from_user")
        event_type = type(event).__name__

        try:
            result = await handler(event, data)
            elapsed = time.monotonic() - start
            user_id = user.id if user else "unknown"
            logger.debug(f"[{event_type}] user={user_id} processed in {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.monotonic() - start
            user_id = user.id if user else "unknown"
            logger.error(f"[{event_type}] user={user_id} error after {elapsed:.3f}s: {e}", exc_info=True)
            raise
