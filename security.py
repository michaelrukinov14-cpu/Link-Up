from __future__ import annotations

import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


ADMIN_PASSWORD_HASH: str = ""


def set_admin_hash(password: str) -> None:
    global ADMIN_PASSWORD_HASH
    ADMIN_PASSWORD_HASH = hash_password(password)


def check_admin_password(password: str) -> bool:
    if not ADMIN_PASSWORD_HASH:
        return False
    return verify_password(password, ADMIN_PASSWORD_HASH)
