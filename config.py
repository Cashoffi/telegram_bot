import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env файла (для локальной разработки)

BOT_TOKEN              = os.environ["BOT_TOKEN"]
ADMIN_ID               = 844320367
DB_PATH                = "bot.db"
