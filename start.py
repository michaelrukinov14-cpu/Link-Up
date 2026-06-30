from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.reply import main_menu_keyboard
from bot.locales import get_string

logger = logging.getLogger(__name__)
router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, lang: str, user_db, session) -> None:
    await state.clear()

    if user_db and not user_db.is_banned:
        if not user_db.is_active:
            await message.answer(
                get_string(lang, "profile_deactivated_msg"),
                reply_markup=main_menu_keyboard(lang),
                parse_mode="HTML",
            )
            return
        await message.answer(
            get_string(lang, "already_registered"),
            reply_markup=main_menu_keyboard(lang),
            parse_mode="HTML",
        )
        return

    args = message.text.split() if message.text else []
    referral_code: str | None = None
    if len(args) > 1:
        potential_code = args[1]
        if potential_code.startswith("ref_"):
            referral_code = potential_code[4:]
        else:
            referral_code = potential_code

    await state.update_data(referral_code=referral_code)

    from bot.locales import detect_language
    tg_user = message.from_user
    detected_lang = detect_language(tg_user.language_code or "ru") if tg_user else "ru"

    await state.update_data(detected_lang=detected_lang)

    await message.answer(
        get_string(detected_lang, "welcome"),
        parse_mode="HTML",
    )
    await message.answer(
        get_string(detected_lang, "register_start"),
        parse_mode="HTML",
    )

    from bot.states.registration import RegistrationStates
    await state.set_state(RegistrationStates.waiting_name)


@router.message(F.text.in_(["🏠 Главное меню", "🏠 Main Menu", "🏠 主菜单"]))
async def main_menu_handler(message: Message, state: FSMContext, lang: str, user_db) -> None:
    await state.clear()
    if not user_db:
        await message.answer(get_string(lang, "no_profile"), parse_mode="HTML")
        return
    await message.answer(
        get_string(lang, "main_menu"),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )
