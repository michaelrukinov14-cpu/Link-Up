from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.locales import get_string


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_search"))
    builder.button(text=get_string(lang, "btn_profile"))
    builder.button(text=get_string(lang, "btn_likes"))
    builder.button(text=get_string(lang, "btn_matches"))
    builder.button(text=get_string(lang, "btn_premium"))
    builder.button(text=get_string(lang, "btn_crystals"))
    builder.button(text=get_string(lang, "btn_referral"))
    builder.button(text=get_string(lang, "btn_settings"))
    builder.button(text=get_string(lang, "btn_help"))
    builder.adjust(2, 2, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def location_keyboard(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="📍 " + ("Отправить геолокацию" if lang == "ru" else ("Send Location" if lang == "en" else "发送位置")), request_location=True)
    builder.button(text=get_string(lang, "btn_skip"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def cancel_keyboard(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_cancel"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
