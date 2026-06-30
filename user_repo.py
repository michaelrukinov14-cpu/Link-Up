from __future__ import annotations

import math
import secrets
import string
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.database.models import GenderEnum, Photo, User


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _generate_referral_code(length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int, load_photos: bool = False) -> Optional[User]:
        stmt = select(User).where(User.telegram_id == telegram_id)
        if load_photos:
            stmt = stmt.options(selectinload(User.photos))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int, load_photos: bool = False) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        if load_photos:
            stmt = stmt.options(selectinload(User.photos))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_referral_code(self, code: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.referral_code == code))
        return result.scalar_one_or_none()

    async def create(
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
        language: str,
        referred_by: Optional[int] = None,
    ) -> User:
        referral_code = _generate_referral_code()
        while await self.get_by_referral_code(referral_code):
            referral_code = _generate_referral_code()

        user = User(
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
            referral_code=referral_code,
            is_active=True,
            is_premium=False,
            is_banned=False,
            warn_count=0,
            crystal_balance=0,
            search_age_min=18,
            search_age_max=99,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, telegram_id: int, **kwargs) -> Optional[User]:
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(**kwargs)
        )
        await self.session.flush()
        return await self.get_by_telegram_id(telegram_id)

    async def deactivate(self, telegram_id: int) -> None:
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(is_active=False)
        )
        await self.session.flush()

    async def activate(self, telegram_id: int) -> None:
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(is_active=True)
        )
        await self.session.flush()

    async def ban(self, telegram_id: int) -> None:
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(is_banned=True, is_active=False)
        )
        await self.session.flush()

    async def unban(self, telegram_id: int) -> None:
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(is_banned=False, is_active=True)
        )
        await self.session.flush()

    async def add_warn(self, telegram_id: int) -> int:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            return 0
        new_count = user.warn_count + 1
        values: dict = {"warn_count": new_count}
        if new_count >= 3:
            values["is_banned"] = True
            values["is_active"] = False
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(**values)
        )
        await self.session.flush()
        return new_count

    async def remove_warn(self, telegram_id: int) -> int:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            return 0
        new_count = max(0, user.warn_count - 1)
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(warn_count=new_count)
        )
        await self.session.flush()
        return new_count

    async def set_premium(self, telegram_id: int, until: datetime) -> None:
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(
                is_premium=True, premium_until=until
            )
        )
        await self.session.flush()

    async def expire_premium(self, telegram_id: int) -> None:
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(
                is_premium=False, premium_until=None
            )
        )
        await self.session.flush()

    async def add_crystals(self, telegram_id: int, amount: int) -> int:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            return 0
        new_balance = user.crystal_balance + amount
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(crystal_balance=new_balance)
        )
        await self.session.flush()
        return new_balance

    async def spend_crystals(self, telegram_id: int, amount: int) -> Optional[int]:
        user = await self.get_by_telegram_id(telegram_id)
        if not user or user.crystal_balance < amount:
            return None
        new_balance = user.crystal_balance - amount
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(crystal_balance=new_balance)
        )
        await self.session.flush()
        return new_balance

    async def count_all(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(User))
        return result.scalar_one()

    async def count_active(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(User).where(User.is_active == True)
        )
        return result.scalar_one()

    async def count_premium(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(User).where(User.is_premium == True)
        )
        return result.scalar_one()

    async def count_banned(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(User).where(User.is_banned == True)
        )
        return result.scalar_one()

    async def count_today(self) -> int:
        today = datetime.now(timezone.utc).date()
        result = await self.session.execute(
            select(func.count()).select_from(User).where(
                func.date(User.created_at) == today
            )
        )
        return result.scalar_one()

    async def search_candidates(
        self,
        viewer: User,
        excluded_ids: List[int],
        limit: int = 20,
    ) -> List[User]:
        conditions = [
            User.telegram_id != viewer.telegram_id,
            User.is_active == True,
            User.is_banned == False,
            User.age >= viewer.search_age_min,
            User.age <= viewer.search_age_max,
        ]
        if viewer.search_gender:
            conditions.append(User.gender == viewer.search_gender)
        if excluded_ids:
            conditions.append(User.telegram_id.not_in(excluded_ids))

        stmt = select(User).where(and_(*conditions)).options(selectinload(User.photos)).limit(limit * 5)
        result = await self.session.execute(stmt)
        candidates = list(result.scalars().all())

        viewer_city = (viewer.city or "").lower()
        for c in candidates:
            c._distance = None
            c._city_match = (c.city or "").lower() == viewer_city
            if viewer.latitude and viewer.longitude and c.latitude and c.longitude:
                c._distance = _haversine(viewer.latitude, viewer.longitude, c.latitude, c.longitude)

        if viewer.search_max_distance:
            candidates = [
                c for c in candidates
                if c._distance is None or c._distance <= viewer.search_max_distance
            ]

        premium = [c for c in candidates if c.is_premium]
        regular = [c for c in candidates if not c.is_premium]

        premium_city = [c for c in premium if c._city_match]
        premium_other = [c for c in premium if not c._city_match]
        regular_city = [c for c in regular if c._city_match]
        regular_other = [c for c in regular if not c._city_match]

        def sort_key(u: User):
            dist = u._distance if u._distance is not None else 99999
            return dist

        premium_city.sort(key=sort_key)
        premium_other.sort(key=sort_key)
        regular_city.sort(key=sort_key)
        regular_other.sort(key=sort_key)

        merged: List[User] = []
        pi = ri = 0
        premium_all = premium_city + premium_other
        regular_all = regular_city + regular_other

        while len(merged) < limit and (pi < len(premium_all) or ri < len(regular_all)):
            if pi < len(premium_all):
                for _ in range(3):
                    if pi < len(premium_all) and len(merged) < limit:
                        merged.append(premium_all[pi])
                        pi += 1
            if ri < len(regular_all) and len(merged) < limit:
                merged.append(regular_all[ri])
                ri += 1

        return merged[:limit]

    async def find_users_by_name_or_id(self, query: str) -> List[User]:
        try:
            tg_id = int(query)
            result = await self.session.execute(
                select(User).where(User.telegram_id == tg_id).options(selectinload(User.photos))
            )
            user = result.scalar_one_or_none()
            return [user] if user else []
        except ValueError:
            pass
        result = await self.session.execute(
            select(User).where(
                or_(
                    User.name.ilike(f"%{query}%"),
                    User.username.ilike(f"%{query}%"),
                )
            ).options(selectinload(User.photos)).limit(10)
        )
        return list(result.scalars().all())
