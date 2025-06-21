from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from aiogram.fsm.context import FSMContext
from typing import Callable, Awaitable, Dict, Any
from database.db_methods import get_user_access_by_tg_id
from bot.states.access_request import AccessRequest
import yaml
import os

# Загрузка сообщений из messages.yaml один раз при старте
MESSAGES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'messages.yaml'))
with open(MESSAGES_PATH, 'r', encoding='utf-8') as f:
    MESSAGES = yaml.safe_load(f)

ALLOWED_COMMANDS = {'/start', '/info', 'ℹ️ Информация', '🔓 Запросить доступ', '↩️ Назад'}

# Список разрешённых состояний FSM (шаги запроса доступа)
FSM_WHITELIST = {
    AccessRequest.waiting_for_name.state,
    AccessRequest.waiting_for_group.state,
    AccessRequest.waiting_for_division.state,
    AccessRequest.waiting_for_confirmation.state,
}


class AccessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # Только для сообщений
        if not isinstance(event, Message):
            return await handler(event, data)

        user = event.from_user
        tg_id = user.id
        text = event.text or ''

        # FSM: разрешённые состояния (например, при вводе имени/группы и т.д.)
        fsm: FSMContext = data.get('state')
        current_state = await fsm.get_state() if fsm else None

        if current_state in FSM_WHITELIST:
            return await handler(event, data)

        # Пропускаем всегда доступные команды/сообщения
        if text.startswith('/start') or text.startswith('/info') or text in ALLOWED_COMMANDS:
            return await handler(event, data)

        # Основная проверка доступа
        access = await get_user_access_by_tg_id(tg_id)

        if access == 'allowed':
            return await handler(event, data)
        elif access == 'denied':
            await event.answer(MESSAGES['access']['denied'])
        elif access == 'requested':
            await event.answer(MESSAGES['access']['requested'])
        else:
            await event.answer(MESSAGES['access']['undefined'])

        return  # Не передаём в хендлер
