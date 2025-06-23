import yaml
import os
from dotenv import load_dotenv

from aiogram import Router, types, F, Bot
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_access_kb, get_access_provision_kb, get_menu_kb, get_admin_kb, get_back_kb
from database import *
from bot.states import AdminPanel

load_dotenv()

router = Router()

messages_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'messages.yaml')
with open(messages_path, 'r', encoding='utf-8') as file:
    MESSAGES = yaml.safe_load(file)


@router.message(F.text == '↩️ Назад')
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(MESSAGES['start']['hello'], reply_markup=await get_access_kb())


@router.callback_query(F.data.startswith("access_"))
async def cmd_access_(callback: CallbackQuery, bot: Bot):
    action, tg_id = callback.data.split("_")[1], int(callback.data.split("_")[2])
    await change_access(tg_id, action)
    await bot.send_message(chat_id=tg_id, text=MESSAGES['access']['allowed'],
                           reply_markup=await get_menu_kb(),
                           disable_web_page_preview=True) if action == 'allow' else await bot.send_message(
        chat_id=tg_id, text=MESSAGES['access']['denied'], disable_web_page_preview=True)
    await callback.message.edit_text(text=f'{callback.message.text}\n'
                                          f'\n'
                                          f'[{action}]', reply_markup=None)
    await callback.answer(
        MESSAGES['admin']['access_allowed'] if action == 'allow' else MESSAGES['admin']['access_denied'])
