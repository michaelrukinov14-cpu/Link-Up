from aiogram.fsm.state import State, StatesGroup


class ProfileEditStates(StatesGroup):
    waiting_new_name = State()
    waiting_new_age = State()
    waiting_new_gender = State()
    waiting_new_city = State()
    waiting_new_bio = State()
    waiting_new_photo = State()
    waiting_delete_photo_num = State()
    waiting_new_voice = State()
    waiting_filter_gender = State()
    waiting_filter_age_min = State()
    waiting_filter_age_max = State()
    waiting_filter_distance = State()
