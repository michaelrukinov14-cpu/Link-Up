from __future__ import annotations

import asyncio
import logging
from typing import Optional, Tuple

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

logger = logging.getLogger(__name__)

_geolocator = Nominatim(user_agent="linkup_bot_v1", timeout=10)


async def geocode_city(city_name: str) -> Optional[Tuple[str, float, float]]:
    loop = asyncio.get_event_loop()
    try:
        location = await loop.run_in_executor(
            None, lambda: _geolocator.geocode(city_name, exactly_one=True, language="ru")
        )
        if location:
            display_name = location.raw.get("display_name", city_name)
            parts = [p.strip() for p in display_name.split(",")]
            short_name = parts[0] if parts else city_name
            return short_name, location.latitude, location.longitude
        return None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        logger.warning(f"Geocoding failed for '{city_name}': {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected geocoding error: {e}")
        return None


async def reverse_geocode(latitude: float, longitude: float) -> Optional[str]:
    loop = asyncio.get_event_loop()
    try:
        location = await loop.run_in_executor(
            None, lambda: _geolocator.reverse((latitude, longitude), exactly_one=True, language="ru")
        )
        if location:
            raw = location.raw.get("address", {})
            city = (
                raw.get("city")
                or raw.get("town")
                or raw.get("village")
                or raw.get("county")
                or raw.get("state")
                or "Неизвестный город"
            )
            return city
        return None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        logger.warning(f"Reverse geocoding failed for ({latitude}, {longitude}): {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected reverse geocoding error: {e}")
        return None
