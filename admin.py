from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    waiting_password = State()
    waiting_user_query = State()
    waiting_ban_reason = State()
    in_panel = State()
