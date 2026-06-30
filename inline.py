from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.locales import get_string


def gender_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "gender_male"), callback_data="gender:male")
    builder.button(text=get_string(lang, "gender_female"), callback_data="gender:female")
    builder.button(text=get_string(lang, "gender_other"), callback_data="gender:other")
    builder.adjust(2, 1)
    return builder.as_markup()


def skip_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_skip"), callback_data="skip")
    return builder.as_markup()


def done_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_done"), callback_data="done")
    return builder.as_markup()


def skip_done_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_skip"), callback_data="skip")
    builder.button(text=get_string(lang, "btn_done"), callback_data="done")
    builder.adjust(2)
    return builder.as_markup()


def profile_edit_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_edit_name"), callback_data="edit:name")
    builder.button(text=get_string(lang, "btn_edit_age"), callback_data="edit:age")
    builder.button(text=get_string(lang, "btn_edit_gender"), callback_data="edit:gender")
    builder.button(text=get_string(lang, "btn_edit_city"), callback_data="edit:city")
    builder.button(text=get_string(lang, "btn_edit_bio"), callback_data="edit:bio")
    builder.button(text=get_string(lang, "btn_edit_photos"), callback_data="edit:photos")
    builder.button(text=get_string(lang, "btn_edit_voice"), callback_data="edit:voice")
    builder.button(text=get_string(lang, "btn_edit_filters"), callback_data="edit:filters")
    builder.button(text=get_string(lang, "btn_delete_profile"), callback_data="edit:delete")
    builder.adjust(2, 2, 2, 2, 1)
    return builder.as_markup()


def search_keyboard(lang: str, candidate_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_like"), callback_data=f"search:like:{candidate_id}")
    builder.button(text=get_string(lang, "btn_dislike"), callback_data=f"search:dislike:{candidate_id}")
    builder.button(text=get_string(lang, "btn_report"), callback_data=f"search:report:{candidate_id}")
    builder.adjust(2, 1)
    return builder.as_markup()


def report_reason_keyboard(lang: str, reported_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_report_spam"), callback_data=f"report:spam:{reported_id}")
    builder.button(text=get_string(lang, "btn_report_fake"), callback_data=f"report:fake:{reported_id}")
    builder.button(text=get_string(lang, "btn_report_insults"), callback_data=f"report:insults:{reported_id}")
    builder.button(text=get_string(lang, "btn_report_content"), callback_data=f"report:content:{reported_id}")
    builder.button(text=get_string(lang, "btn_report_other"), callback_data=f"report:other:{reported_id}")
    builder.button(text=get_string(lang, "btn_cancel"), callback_data="report:cancel")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


def skip_report_comment_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_skip"), callback_data="report_comment:skip")
    builder.button(text=get_string(lang, "btn_cancel"), callback_data="report:cancel")
    builder.adjust(2)
    return builder.as_markup()


def premium_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    from bot.config import config
    builder = InlineKeyboardBuilder()
    builder.button(
        text=get_string(lang, "btn_premium_1m", stars=config.premium_1m_stars, crystals=config.premium_1m_crystals),
        callback_data="premium:plan:month"
    )
    builder.button(
        text=get_string(lang, "btn_premium_1y", stars=config.premium_1y_stars, crystals=config.premium_1y_crystals),
        callback_data="premium:plan:year"
    )
    builder.adjust(1)
    return builder.as_markup()


def premium_payment_keyboard(lang: str, plan: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_buy_stars"), callback_data=f"premium:pay:stars:{plan}")
    builder.button(text=get_string(lang, "btn_buy_crystals"), callback_data=f"premium:pay:crystals:{plan}")
    if True:
        builder.button(text=get_string(lang, "btn_buy_card"), callback_data=f"premium:pay:card:{plan}")
    builder.button(text=get_string(lang, "btn_back"), callback_data="premium:back")
    builder.adjust(1)
    return builder.as_markup()


def crystals_buy_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_buy_crystals_10"), callback_data="crystals:buy:10")
    builder.button(text=get_string(lang, "btn_buy_crystals_50"), callback_data="crystals:buy:50")
    builder.button(text=get_string(lang, "btn_buy_crystals_100"), callback_data="crystals:buy:100")
    builder.button(text=get_string(lang, "btn_crystals_history"), callback_data="crystals:history")
    builder.adjust(1)
    return builder.as_markup()


def filter_gender_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "gender_male"), callback_data="filter:gender:male")
    builder.button(text=get_string(lang, "gender_female"), callback_data="filter:gender:female")
    builder.button(text=get_string(lang, "gender_other"), callback_data="filter:gender:other")
    builder.button(text=get_string(lang, "filter_gender_any"), callback_data="filter:gender:any")
    builder.adjust(2, 1, 1)
    return builder.as_markup()


def filters_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_filter_gender"), callback_data="filter:set:gender")
    builder.button(text=get_string(lang, "btn_filter_age"), callback_data="filter:set:age")
    builder.button(text=get_string(lang, "btn_filter_distance"), callback_data="filter:set:distance")
    builder.button(text=get_string(lang, "btn_back"), callback_data="profile:menu")
    builder.adjust(1)
    return builder.as_markup()


def language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data="lang:ru")
    builder.button(text="🇬🇧 English", callback_data="lang:en")
    builder.button(text="🇨🇳 中文", callback_data="lang:zh")
    builder.adjust(1)
    return builder.as_markup()


def confirm_keyboard(lang: str, confirm_cb: str, cancel_cb: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_yes"), callback_data=confirm_cb)
    builder.button(text=get_string(lang, "btn_no"), callback_data=cancel_cb)
    builder.adjust(2)
    return builder.as_markup()


def photos_manage_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_add_photo"), callback_data="photos:add")
    builder.button(text=get_string(lang, "btn_delete_photo"), callback_data="photos:delete")
    builder.button(text=get_string(lang, "btn_back"), callback_data="profile:menu")
    builder.adjust(2, 1)
    return builder.as_markup()


def admin_panel_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "admin_btn_stats"), callback_data="admin:stats")
    builder.button(text=get_string(lang, "admin_btn_find_user"), callback_data="admin:find_user")
    builder.button(text=get_string(lang, "admin_btn_reports"), callback_data="admin:reports")
    builder.adjust(1)
    return builder.as_markup()


def admin_user_action_keyboard(lang: str, tg_id: int, is_banned: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_banned:
        builder.button(text=get_string(lang, "admin_btn_unban"), callback_data=f"admin:unban:{tg_id}")
    else:
        builder.button(text=get_string(lang, "admin_btn_ban"), callback_data=f"admin:ban:{tg_id}")
    builder.button(text=get_string(lang, "admin_btn_warn"), callback_data=f"admin:warn:{tg_id}")
    builder.button(text=get_string(lang, "admin_btn_remove_warn"), callback_data=f"admin:unwarn:{tg_id}")
    builder.button(text=get_string(lang, "admin_btn_delete_profile"), callback_data=f"admin:del_profile:{tg_id}")
    builder.button(text=get_string(lang, "btn_back"), callback_data="admin:back")
    builder.adjust(1)
    return builder.as_markup()


def back_keyboard(lang: str, callback: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_back"), callback_data=callback)
    return builder.as_markup()


def menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_menu"), callback_data="main:menu")
    return builder.as_markup()


def activate_profile_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_string(lang, "btn_activate_profile"), callback_data="profile:activate")
    return builder.as_markup()
