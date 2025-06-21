from aiogram import types


async def get_name_kb():
    k = [
        [types.KeyboardButton(text='↩️ Назад'), ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="фио",
        is_persistent=False
    )
    return keyboard


async def get_group_kb():
    k = [
        [types.KeyboardButton(text='Сотрудник')],
        [types.KeyboardButton(text='↩️ Назад')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="номер группы",
        is_persistent=False,
    )
    return keyboard


async def get_division_kb():
    k = [
        [types.KeyboardButton(text='Не планирую')],
        [types.KeyboardButton(text='↩️ Назад')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="подразделение",
        is_persistent=False,
    )
    return keyboard


async def get_confirmation_kb():
    k = [
        [types.KeyboardButton(text='Всё верно')],
        [types.KeyboardButton(text='↩️ Заполнить заново')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="получите доступ",
        is_persistent=False
    )
    return keyboard
