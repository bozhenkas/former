import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def check_database():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/former"))
    db = client.get_database()
    
    print("🔍 Проверка базы данных...")
    print("=" * 50)
    
    try:
        # Проверяем коллекции
        collections = await db.list_collection_names()
        print(f"📁 Коллекции в БД: {collections}")
        print()
        
        # Проверяем индексы
        print("📊 Проверка индексов:")
        for collection_name in ['users', 'google_accounts', 'integrations', 'form_responses']:
            if collection_name in collections:
                indexes = await db[collection_name].list_indexes().to_list(length=None)
                print(f"  {collection_name}: {len(indexes)} индексов")
                for idx in indexes:
                    print(f"    - {idx['name']}: {idx['key']}")
            else:
                print(f"  {collection_name}: коллекция не найдена!")
        print()
        
        # Проверяем данные
        print("📋 Статистика данных:")
        for collection_name in collections:
            count = await db[collection_name].count_documents({})
            print(f"  {collection_name}: {count} документов")
        print()
        
        # Проверяем связи
        print("🔗 Проверка связей:")
        
        # Интеграции -> Google аккаунты
        integrations = await db.integrations.find().to_list(length=5)
        for integration in integrations:
            google_account = await db.google_accounts.find_one({"_id": integration.get("google_account_id")})
            if google_account:
                print(f"  ✅ Интеграция {integration['integration_name']} -> Google аккаунт найден")
            else:
                print(f"  ❌ Интеграция {integration['integration_name']} -> Google аккаунт НЕ найден!")
        
        # Form responses -> Integrations
        responses = await db.form_responses.find().to_list(length=5)
        for response in responses:
            integration = await db.integrations.find_one({"_id": response.get("integration_id")})
            if integration:
                print(f"  ✅ Response {response['_id']} -> Интеграция найдена")
            else:
                print(f"  ❌ Response {response['_id']} -> Интеграция НЕ найдена!")
        
        print()
        print("✅ Проверка завершена!")
        
    except Exception as e:
        print(f"❌ Ошибка при проверке БД: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_database()) 