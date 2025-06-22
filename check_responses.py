import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def check_responses():
    # Подключение к MongoDB
    client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/former"))
    db = client.get_database()
    
    try:
        # Получаем все ответы
        responses = await db.form_responses.find().to_list(length=10)
        
        print(f"📊 Найдено {len(responses)} записей в form_responses:")
        print("-" * 50)
        
        for i, response in enumerate(responses, 1):
            print(f"Запись #{i}:")
            print(f"  ID: {response['_id']}")
            print(f"  Integration ID: {response['integration_id']}")
            print(f"  Form ID: {response['form_id']}")
            print(f"  Status: {response['status']}")
            print(f"  Received at: {response['received_at']}")
            if 'error_message' in response and response['error_message']:
                print(f"  Error: {response['error_message']}")
            print(f"  Data: {response['response_data']}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_responses()) 