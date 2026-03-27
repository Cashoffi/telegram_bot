import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, WEBHOOK_PORT
from database import init_db
from handlers import common, bug_report, idea, admin, lists
from donation_webhook import create_app

logging.basicConfig(level=logging.INFO)


async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp  = Dispatcher(storage=MemoryStorage())

    dp.include_router(admin.router)
    dp.include_router(common.router)
    dp.include_router(bug_report.router)
    dp.include_router(idea.router)
    dp.include_router(lists.router)

    # Веб-сервер для вебхука DonationAlerts
    app = create_app(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", WEBHOOK_PORT)
    await site.start()
    logging.info(f"Donation webhook слушает на порту {WEBHOOK_PORT} → /donation")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
