import yaml
import os
from dotenv import load_dotenv

from aiogram import Router, types, F, Bot
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery

from bot.keyboards import get_access_kb, get_access_provision_kb, get_menu_kb
from database import *

load_dotenv()

router = Router()

with open('messages.yaml', 'r', encoding='utf-8') as file:
    MESSAGES = yaml.safe_load(file)


@router.message(F.text == '↩️ Назад')
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(MESSAGES['start']['hello'], reply_markup=await get_access_kb())


@router.message(F.text == '🔓 Запросить доступ')
async def msg_access_request(message: types.Message, bot: Bot):
    print('penis')
    if await access_requested(message.from_user.id):
        await message.answer(MESSAGES['access']['requested'])
        user_data = ((await get_user_by_tg_id(message.from_user.id))['tg_username'],
                     (await get_user_by_tg_id(message.from_user.id))['tg_id'],
                     (await get_user_by_tg_id(message.from_user.id))['name'],
                     (await get_user_by_tg_id(message.from_user.id))['group'],
                     (await get_user_by_tg_id(message.from_user.id))['division'],
                     )
        print(user_data)
        await bot.send_message(chat_id=os.getenv("ADMIN_ID"), text=MESSAGES['admin']['access'].format(*user_data),
                               reply_markup=await get_access_provision_kb(message.from_user.id))
    else:
        await message.answer(MESSAGES['access'][f"{await get_user_access_by_tg_id(message.from_user.id)}"])


@router.callback_query(F.data.startswith("access_"))
async def cmd_access_(callback: CallbackQuery, bot: Bot):
    action, tg_id = callback.data.split("_")[1], int(callback.data.split("_")[2])
    await change_access(tg_id, action)
    await bot.send_message(chat_id=tg_id, text=MESSAGES['access']['allowed'],
                           reply_markup=await get_menu_kb()) if action == 'allow' else await bot.send_message(
        chat_id=tg_id, text=MESSAGES['access']['denied'])
    await callback.message.edit_text(text=f'{callback.message.text}\n'
                                          f'\n'
                                          f'[{action}]', reply_markup=None)
    await callback.answer(MESSAGES['admin']['access_allowed'] if action == 'allow' else MESSAGES['admin']['access_denied'])
