from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    bot_token: str
    admin_password: str
    admin_ids: List[int]
    database_url: str
    redis_url: str
    payment_provider_token: str
    premium_1m_stars: int
    premium_1y_stars: int
    premium_1m_crystals: int
    premium_1y_crystals: int
    throttle_rate: float
    throttle_key_prefix: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Config":
        admin_ids_raw = os.getenv("ADMIN_IDS", "")
        admin_ids = [int(x.strip()) for x in admin_ids_raw.split(",") if x.strip().isdigit()]
        return cls(
            bot_token=os.environ["BOT_TOKEN"],
            admin_password=os.environ["ADMIN_PASSWORD"],
            admin_ids=admin_ids,
            database_url=os.environ["DATABASE_URL"],
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            payment_provider_token=os.getenv("PAYMENT_PROVIDER_TOKEN", ""),
            premium_1m_stars=int(os.getenv("PREMIUM_1M_STARS", "50")),
            premium_1y_stars=int(os.getenv("PREMIUM_1Y_STARS", "250")),
            premium_1m_crystals=int(os.getenv("PREMIUM_1M_CRYSTALS", "50")),
            premium_1y_crystals=int(os.getenv("PREMIUM_1Y_CRYSTALS", "250")),
            throttle_rate=float(os.getenv("THROTTLE_RATE", "0.5")),
            throttle_key_prefix=os.getenv("THROTTLE_KEY_PREFIX", "throttle:"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


config: Config = Config.from_env()
