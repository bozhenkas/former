"""клавиатуры для главного меню и начальной регистрации пользователя"""

from aiogram import types


async def get_start_kb():
    k = [
        [types.KeyboardButton(text='Начать регистрацию'), ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку",
        is_persistent=False,
        one_time_keyboard=True
    )
    return keyboard


async def get_access_kb():
    k = [
        [types.KeyboardButton(text='🔓 Запросить доступ'), ],
        [types.KeyboardButton(text='ℹ️ Информация'), ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="получите доступ",
        is_persistent=False
    )
    return keyboard


async def get_back_kb():
    k = [
        [types.KeyboardButton(text='↩️ Назад'), ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="получите доступ",
        is_persistent=False
    )
    return keyboard
