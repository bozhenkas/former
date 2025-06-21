import yaml
import os
from dotenv import load_dotenv

from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext

from database import *
from bot.keyboards import get_name_kb, get_group_kb, get_division_kb, get_confirmation_kb, get_access_provision_kb
from bot.states import AccessRequest

load_dotenv()

router = Router()

with open('messages.yaml', 'r', encoding='utf-8') as file:
    MESSAGES = yaml.safe_load(file)


@router.message(F.text == '🔓 Запросить доступ')
async def msg_access_request(message: types.Message, state: FSMContext):
    if await get_user_access_by_tg_id(message.from_user.id) != 'undefined':
        await message.answer(MESSAGES['access'][f"{await get_user_access_by_tg_id(message.from_user.id)}"])
        return
    await message.answer(MESSAGES['access_request']['info'])
    await message.answer(MESSAGES['access_request']['name'], reply_markup=await get_name_kb(),
                         disable_notification=True)
    await state.set_state(AccessRequest.waiting_for_name)


@router.message(AccessRequest.waiting_for_name)
async def access_get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await message.answer(MESSAGES['access_request']['group'], reply_markup=await get_group_kb())
    await state.set_state(AccessRequest.waiting_for_group)


@router.message(AccessRequest.waiting_for_group)
async def access_get_group(message: types.Message, state: FSMContext):
    if message.text == "↩️ Назад":
        await state.set_state(AccessRequest.waiting_for_name)
        await message.answer(MESSAGES['access_request']['name'], reply_markup=await get_name_kb())
        return
    await state.update_data(group=message.text.replace(' ', '').upper())
    await message.answer(MESSAGES['access_request']['division'], reply_markup=await get_division_kb())
    await state.set_state(AccessRequest.waiting_for_division)


@router.message(AccessRequest.waiting_for_division)
async def access_get_division(message: types.Message, state: FSMContext):
    if message.text == "↩️ Назад":
        await state.set_state(AccessRequest.waiting_for_group)
        await message.answer(MESSAGES['access_request']['group'], reply_markup=await get_group_kb())
        return
    await state.update_data(division=message.text)
    data = await state.get_data()
    await message.answer(MESSAGES['access_request']['confirmation'].format(name=data['name'], group=data['group'],
                                                                           division=data['division']),
                         reply_markup=await get_confirmation_kb())
    await state.set_state(AccessRequest.waiting_for_confirmation)


@router.message(AccessRequest.waiting_for_confirmation)
async def access_get_confirmation(message: types.Message, state: FSMContext, bot: Bot):
    if message.text == "↩️ Заполнить заново":
        await state.set_state(AccessRequest.waiting_for_name)
        await message.answer(MESSAGES['access_request']['name'], reply_markup=await get_name_kb())
        return
    await access_requested(message.from_user.id)
    await message.answer(MESSAGES['access']['requested'], reply_markup=types.ReplyKeyboardRemove())
    data = await state.get_data()
    await state.clear()
    await add_user_data(tg_id=message.from_user.id, name=data['name'], group=data['group'], division=data['division'])
    user_data = (message.from_user.username, message.from_user.id, data['name'], data['group'], data['division'])
    await bot.send_message(chat_id=os.getenv("ADMIN_ID"), text=MESSAGES['admin']['access'].format(*user_data),
                           reply_markup=await get_access_provision_kb(message.from_user.id))
