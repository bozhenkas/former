from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


async def get_access_provision_kb(tg_id: int):
    buttons = [[InlineKeyboardButton(text='Разрешить', callback_data=f'access_allow_{tg_id}'),
                InlineKeyboardButton(text='Запретить', callback_data=f'access_deny_{tg_id}')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_admin_kb():
    # Заглушка для совместимости
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Админ панель")]], resize_keyboard=True)
