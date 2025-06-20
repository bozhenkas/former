"""обработчик команды /start, регистрация новых пользователей и навигация по главному меню"""

import yaml
import os

from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot import get_access_kb, get_start_kb, get_back_kb

# создание роутера
router = Router()

# загрузка сообщений
with open('messages.yaml', 'r', encoding='utf-8') as file:
    MESSAGES = yaml.safe_load(file)


@router.message(F.text == '↩️ Назад')
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(MESSAGES['start']['hello'], reply_markup=await get_access_kb())


@router.message(F.text == 'ℹ️ Информация')
async def msg_info(message: types.Message):
    await message.answer(MESSAGES['start']['info'], reply_markup=await get_back_kb())
