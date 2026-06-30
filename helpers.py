from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from bot.database.models import Photo, User
from bot.locales import get_string


def format_user_profile(user: User, lang: str, show_distance: bool = False, distance: Optional[float] = None) -> str:
    name = user.name
    age = user.age
    city = user.city or "—"
    bio = user.bio or get_string(lang, "profile_no_bio")
    premium_line = "⭐ Premium\n" if user.is_premium else ""

    if show_distance:
        if distance is not None:
            if distance < 1:
                dist_str = get_string(lang, "distance_same_city")
            else:
                dist_str = get_string(lang, "distance_km", dist=distance)
        else:
            dist_str = get_string(lang, "distance_unknown")
        return (
            f"👤 <b>{name}</b>, {age} {'лет' if lang == 'ru' else ('years old' if lang == 'en' else '岁')}\n"
            f"🏙 {city}\n"
            f"📏 {dist_str}\n"
            f"📖 {bio}\n"
            f"\n{premium_line}"
        )

    return (
        f"👤 <b>{name}</b>, {age} {'лет' if lang == 'ru' else ('years old' if lang == 'en' else '岁')}\n"
        f"🏙 {city}\n"
        f"📖 {bio}\n"
        f"\n{premium_line}"
    )


def get_user_link(user: User) -> str:
    if user.username:
        return f"<a href='https://t.me/{user.username}'>@{user.username}</a>"
    return f"<a href='tg://user?id={user.telegram_id}'>ID:{user.telegram_id}</a>"


def is_premium_active(user: User) -> bool:
    if not user.is_premium or not user.premium_until:
        return False
    return user.premium_until > datetime.now(timezone.utc)


def get_first_photo(user: User) -> Optional[str]:
    if user.photos:
        sorted_photos = sorted(user.photos, key=lambda p: p.position)
        return sorted_photos[0].file_id if sorted_photos else None
    return None


def format_datetime(dt: datetime, lang: str) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%d.%m.%Y %H:%M")
