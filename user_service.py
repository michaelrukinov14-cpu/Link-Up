from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import GenderEnum, User
from bot.database.repositories import PhotoRepository, UserRepository
from bot.locales import detect_language

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.photo_repo = PhotoRepository(session)

    async def get_user(self, telegram_id: int, load_photos: bool = False) -> Optional[User]:
        return await self.user_repo.get_by_telegram_id(telegram_id, load_photos=load_photos)

    async def create_user(
        self,
        telegram_id: int,
        username: Optional[str],
        name: str,
        age: int,
        gender: GenderEnum,
        city: Optional[str],
        latitude: Optional[float],
        longitude: Optional[float],
        bio: Optional[str],
        lang_code: Optional[str],
        referral_code: Optional[str] = None,
    ) -> User:
        language = detect_language(lang_code or "ru")
        referred_by: Optional[int] = None

        if referral_code:
            referrer = await self.user_repo.get_by_referral_code(referral_code)
            if referrer and referrer.telegram_id != telegram_id:
                referred_by = referrer.telegram_id

        async with self.session.begin_nested():
            user = await self.user_repo.create(
                telegram_id=telegram_id,
                username=username,
                name=name,
                age=age,
                gender=gender,
                city=city,
                latitude=latitude,
                longitude=longitude,
                bio=bio,
                language=language,
                referred_by=referred_by,
            )
        await self.session.commit()
        logger.info(f"Created user {telegram_id} ({name})")
        return user

    async def update_user(self, telegram_id: int, **kwargs) -> Optional[User]:
        async with self.session.begin_nested():
            user = await self.user_repo.update(telegram_id, **kwargs)
        await self.session.commit()
        return user

    async def deactivate_user(self, telegram_id: int) -> None:
        async with self.session.begin_nested():
            await self.user_repo.deactivate(telegram_id)
        await self.session.commit()

    async def activate_user(self, telegram_id: int) -> None:
        async with self.session.begin_nested():
            await self.user_repo.activate(telegram_id)
        await self.session.commit()

    async def add_photo(self, user_id: int, file_id: str) -> Optional[int]:
        position = await self.photo_repo.get_next_position(user_id)
        if position is None:
            return None
        async with self.session.begin_nested():
            await self.photo_repo.add_photo(user_id=user_id, file_id=file_id, position=position)
        await self.session.commit()
        return position

    async def delete_photo(self, user_id: int, position: int) -> bool:
        async with self.session.begin_nested():
            result = await self.photo_repo.delete_photo(user_id=user_id, position=position)
        await self.session.commit()
        return result

    async def get_photos_count(self, user_id: int) -> int:
        return await self.photo_repo.count_photos(user_id)

    async def exists(self, telegram_id: int) -> bool:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        return user is not None
