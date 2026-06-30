from typing import Any, Dict

from bot.locales.en import STRINGS as EN_STRINGS
from bot.locales.ru import STRINGS as RU_STRINGS
from bot.locales.zh import STRINGS as ZH_STRINGS

LOCALES: Dict[str, Dict[str, Any]] = {
    "ru": RU_STRINGS,
    "en": EN_STRINGS,
    "zh": ZH_STRINGS,
}

SUPPORTED_LANGUAGES = list(LOCALES.keys())


def get_string(lang: str, key: str, **kwargs) -> str:
    strings = LOCALES.get(lang, LOCALES["ru"])
    template = strings.get(key, LOCALES["ru"].get(key, key))
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template
    return template


def detect_language(lang_code: str) -> str:
    if not lang_code:
        return "ru"
    code = lang_code.lower()[:2]
    if code in SUPPORTED_LANGUAGES:
        return code
    return "ru"
