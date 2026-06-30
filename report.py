from aiogram.fsm.state import State, StatesGroup


class ReportStates(StatesGroup):
    waiting_reason = State()
    waiting_comment = State()
