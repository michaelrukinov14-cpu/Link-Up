from __future__ import annotations

from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Photo, User


class PhotoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_photos(self, user_id: int) -> List[Photo]:
        result = await self.session.execute(
            select(Photo).where(Photo.user_id == user_id).order_by(Photo.position)
        )
        return list(result.scalars().all())

    async def add_photo(self, user_id: int, file_id: str, position: int) -> Photo:
        photo = Photo(user_id=user_id, file_id=file_id, position=position)
        self.session.add(photo)
        await self.session.flush()
        return photo

    async def delete_photo(self, user_id: int, position: int) -> bool:
        result = await self.session.execute(
            delete(Photo).where(Photo.user_id == user_id, Photo.position == position)
        )
        await self.session.flush()
        return result.rowcount > 0

    async def delete_all_photos(self, user_id: int) -> None:
        await self.session.execute(delete(Photo).where(Photo.user_id == user_id))
        await self.session.flush()

    async def count_photos(self, user_id: int) -> int:
        result = await self.session.execute(
            select(Photo).where(Photo.user_id == user_id)
        )
        return len(result.scalars().all())

    async def get_next_position(self, user_id: int) -> Optional[int]:
        photos = await self.get_user_photos(user_id)
        occupied = {p.position for p in photos}
        for pos in range(3):
            if pos not in occupied:
                return pos
        return None
