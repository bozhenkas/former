from database import db
from datetime import datetime

async def get_user_by_telegram_id(telegram_id: int) -> dict | None:
    """
    Получить все данные пользователя по telegram_id.
    """
    return await db.users.find_one({"telegram_id": telegram_id})

async def get_user_access_by_telegram_id(telegram_id: int) -> str:
    """
    Получить статус access пользователя по telegram_id.
    Возвращает: 'allowed', 'denied', 'undefined' (по умолчанию).
    """
    user = await db.users.find_one({"telegram_id": telegram_id})
    if user:
        return user.get("access", "undefined")
    return "undefined"

async def add_user(telegram_id: int, telegram_username: str | None) -> None:
    """
    Добавить пользователя в базу данных. access по умолчанию 'undefined'.
    """
    await db.users.insert_one({
        "telegram_id": telegram_id,
        "telegram_username": telegram_username,
        "access": "undefined",
        "name": None,
        "group": None,
        "division": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

async def add_user_if_not_exists(telegram_id: int, telegram_username: str | None) -> None:
    """
    Добавить пользователя, если его нет в базе.
    """
    user = await db.users.find_one({"telegram_id": telegram_id})
    if not user:
        await add_user(telegram_id, telegram_username)

async def add_user_data(telegram_id: int, name: str = None, group: str = None, division: str = None) -> None:
    """
    Обновить name, group, division пользователя по telegram_id.
    """
    await db.users.update_one(
        {"telegram_id": telegram_id},
        {"$set": {"name": name, "group": group, "division": division, "updated_at": datetime.utcnow()}}
    ) 