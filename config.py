import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env файла (для локальной разработки)

BOT_TOKEN              = os.environ["BOT_TOKEN"]
ADMIN_ID               = 844320367
DB_PATH                = os.environ.get("DB_PATH", "bot.db")  # На хостинге: /app/data/bot.db
DONATIONALERTS_SECRET = os.environ.get("DONATIONALERTS_SECRET", "")  # Secret Key из настроек DA
WEBHOOK_PORT          = int(os.environ.get("WEBHOOK_PORT", "8080"))   # Порт HTTP-сервера
