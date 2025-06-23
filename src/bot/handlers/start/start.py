import yaml
import os

from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from database import user_in_base, get_user_access_by_tg_id
from bot.keyboards import get_access_kb, get_back_kb, get_menu_kb

# создание роутера
router = Router()

# загрузка сообщений
messages_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'bot', 'messages.yaml')
with open(messages_path, 'r', encoding='utf-8') as file:
    MESSAGES = yaml.safe_load(file)


@router.message(F.text == '↩️ Назад')
@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    if not await user_in_base(message.from_user.id):
        await message.answer(MESSAGES['start']['hello'], reply_markup=await get_access_kb())
    else:
        access = await get_user_access_by_tg_id(message.from_user.id)
        if access == 'allowed':
            # menu_kb = await get_menu_kb()  # если есть функция
            await message.answer(MESSAGES['start']['menu'], reply_markup=await get_menu_kb())
        elif access == 'undefined':
            await message.answer(MESSAGES['start']['hello'], reply_markup=await get_access_kb())
        elif access == 'denied':
            await message.answer(MESSAGES['access']['denied'], reply_markup=types.ReplyKeyboardRemove())
        elif access == 'requested':
            await message.answer(MESSAGES['access']['requested'])


@router.message(F.text == 'ℹ️ Информация')
@router.message(Command('info'))
async def msg_info(message: types.Message):
    await message.answer(MESSAGES['start']['info'], reply_markup=await get_back_kb())
