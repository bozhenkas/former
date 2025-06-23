import os
from dotenv import load_dotenv

load_dotenv()
 
class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    # Добавьте другие переменные окружения по мере необходимости 