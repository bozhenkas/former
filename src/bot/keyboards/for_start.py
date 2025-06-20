"""клавиатуры для главного меню и начальной регистрации пользователя"""

from aiogram import types


async def get_menu_kb():
    k = [
        [types.KeyboardButton(text='Кнопки'), types.KeyboardButton(text='Будущего')],
        [types.KeyboardButton(text='Меню')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="welcome",
        is_persistent=False,
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
