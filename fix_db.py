import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def fix_database():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/former"))
    db = client.get_database()
    
    print("🔧 Исправление базы данных...")
    print("=" * 50)
    
    try:
        # 1. Добавляем недостающие индексы
        print("📊 Добавление индексов:")
        
        # Уникальный индекс на tg_id в users
        try:
            await db.users.create_index("tg_id", unique=True)
            print("  ✅ Уникальный индекс на tg_id в users создан")
        except Exception as e:
            print(f"  ⚠️  Индекс на tg_id уже существует или ошибка: {e}")
        
        # Индекс на webhook_token в integrations
        try:
            await db.integrations.create_index("webhook_token", unique=True)
            print("  ✅ Уникальный индекс на webhook_token в integrations создан")
        except Exception as e:
            print(f"  ⚠️  Индекс на webhook_token уже существует или ошибка: {e}")
        
        # Индекс на user_tg_id в google_accounts (если нет)
        try:
            await db.google_accounts.create_index("user_tg_id")
            print("  ✅ Индекс на user_tg_id в google_accounts создан")
        except Exception as e:
            print(f"  ⚠️  Индекс на user_tg_id уже существует или ошибка: {e}")
        
        print()
        
        # 2. Очищаем некорректные данные
        print("🧹 Очистка некорректных данных:")
        
        # Удаляем интеграции без Google аккаунтов
        integrations_without_google = []
        async for integration in db.integrations.find():
            google_account = await db.google_accounts.find_one({"_id": integration.get("google_account_id")})
            if not google_account:
                integrations_without_google.append(integration["_id"])
        
        if integrations_without_google:
            result = await db.integrations.delete_many({"_id": {"$in": integrations_without_google}})
            print(f"  🗑️  Удалено {result.deleted_count} интеграций без Google аккаунтов")
        else:
            print("  ✅ Все интеграции имеют связанные Google аккаунты")
        
        # Удаляем form_responses без интеграций
        responses_without_integration = []
        async for response in db.form_responses.find():
            integration = await db.integrations.find_one({"_id": response.get("integration_id")})
            if not integration:
                responses_without_integration.append(response["_id"])
        
        if responses_without_integration:
            result = await db.form_responses.delete_many({"_id": {"$in": responses_without_integration}})
            print(f"  🗑️  Удалено {result.deleted_count} ответов без интеграций")
        else:
            print("  ✅ Все ответы имеют связанные интеграции")
        
        print()
        print("✅ Исправление завершено!")
        
    except Exception as e:
        print(f"❌ Ошибка при исправлении БД: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(fix_database()) 