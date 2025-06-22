import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

async def add_test_integration():
    # Подключение к MongoDB
    client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/former"))
    db = client.get_database()
    
    # Получаем API URL из переменных окружения
    api_url = os.getenv("API_URL", "http://localhost:8000")
    
    # Создаем тестовую интеграцию
    test_integration = {
        "user_tg_id": 123456,
        "integration_name": "Test Integration",
        "webhook_token": "TEST_TOKEN",
        "form_id": "form123",
        "google_sheet_id": "sheet123",
        "google_account_id": ObjectId(),
        "field_mapping": {"name": "A", "email": "B"},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    try:
        # Добавляем интеграцию
        result = await db.integrations.insert_one(test_integration)
        print(f"✅ Тестовая интеграция добавлена с ID: {result.inserted_id}")
        print(f"🔗 Webhook URL: {api_url}/api/v1/yandex/webhook?token=TEST_TOKEN")
        
        # Проверяем, что интеграция найдется
        found = await db.integrations.find_one({"webhook_token": "TEST_TOKEN"})
        if found:
            print("✅ Интеграция успешно найдена в базе")
        else:
            print("❌ Ошибка: интеграция не найдена")
            
    except Exception as e:
        print(f"❌ Ошибка при добавлении интеграции: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(add_test_integration()) 