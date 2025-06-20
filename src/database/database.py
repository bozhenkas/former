from motor.motor_asyncio import AsyncIOMotorClient
from .config import Config
from .models import setup_indexes

client = AsyncIOMotorClient(Config.MONGO_URI)
db = client.get_default_database()

async def init_db():
    await setup_indexes(db) 