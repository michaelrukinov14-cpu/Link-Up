from aiogram.fsm.state import State, StatesGroup


class PaymentStates(StatesGroup):
    waiting_premium_plan = State()
    waiting_crystals_amount = State()
