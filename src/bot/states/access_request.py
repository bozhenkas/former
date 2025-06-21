from aiogram.fsm.state import State, StatesGroup


class AccessRequest(StatesGroup):
    waiting_for_name = State()
    waiting_for_group = State()
    waiting_for_division = State()
    waiting_for_confirmation = State()
