from database import db
from datetime import datetime


async def get_user_by_tg_id(tg_id: int) -> dict | None:
    return await db.users.find_one({"tg_id": tg_id})


async def get_user_access_by_tg_id(tg_id: int):
    user = await db.users.find_one({"tg_id": tg_id})
    return user["access"] if user else None


async def add_user(tg_id: int, tg_username: str | None) -> None:
    await db.users.insert_one({
        "tg_id": tg_id,
        "tg_username": tg_username,
        "access": "undefined",
        "name": None,
        "group": None,
        "division": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })


async def add_user_if_not_exists(tg_id: int, tg_username: str | None) -> None:
    user = await db.users.find_one({"tg_id": tg_id})
    if not user:
        await add_user(tg_id, tg_username)


async def add_user_data(tg_id: int, name: str = None, group: str = None, division: str = None) -> None:
    await db.users.update_one(
        {"tg_id": tg_id},
        {"$set": {"name": name, "group": group, "division": division, "updated_at": datetime.utcnow()}}
    )


async def access_requested(tg_id: int) -> bool:
    user = await db.users.find_one({"tg_id": tg_id})
    if not user:
        return False
    access = user.get("access", "undefined")
    if access == "undefined":
        await db.users.update_one(
            {"tg_id": tg_id},
            {"$set": {"access": "requested", "updated_at": datetime.utcnow()}}
        )
        return True
    elif access == "requested":
        return False
    return True


async def user_in_base(tg_id: int) -> bool:
    if await db.users.find_one({"tg_id": tg_id}):
        return True
    else:
        return False


async def change_access(tg_id: int, action: str) -> bool:
    """
    Изменить статус access пользователя по tg_id.
    action: 'allow' -> 'allowed', 'deny' -> 'denied'
    Возвращает True, если обновление прошло успешно, иначе False.
    """
    if action == 'allow':
        new_status = 'allowed'
    elif action == 'deny':
        new_status = 'denied'
    else:
        return False
    result = await db.users.update_one(
        {"tg_id": tg_id},
        {"$set": {"access": new_status, "updated_at": datetime.utcnow()}}
    )
    return result.modified_count > 0
