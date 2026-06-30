from __future__ import annotations

import re
from typing import Optional


def validate_name(name: str) -> bool:
    return 1 <= len(name.strip()) <= 100


def validate_age(age_str: str) -> Optional[int]:
    try:
        age = int(age_str.strip())
        if 11 <= age <= 120:
            return age
        return None
    except ValueError:
        return None


def validate_bio(bio: str) -> bool:
    return len(bio) <= 500


def validate_filter_age(age_str: str) -> Optional[int]:
    try:
        age = int(age_str.strip())
        if 11 <= age <= 120:
            return age
        return None
    except ValueError:
        return None


def validate_filter_distance(distance_str: str) -> Optional[int]:
    try:
        d = int(distance_str.strip())
        if d >= 0:
            return d
        return None
    except ValueError:
        return None


def sanitize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"<[^>]+>", "", text)
    return text
