import logging
from aiohttp import web
from aiogram import Bot
from config import DONATIONALERTS_SECRET, ADMIN_ID

logger = logging.getLogger(__name__)


async def handle_donation(request: web.Request, bot: Bot) -> web.Response:
    try:
        data = await request.post()
    except Exception:
        return web.Response(status=400)

    # Проверка секретного ключа
    if DONATIONALERTS_SECRET and data.get("secret_key", "") != DONATIONALERTS_SECRET:
        logger.warning("Donation webhook: неверный secret_key")
        return web.Response(status=403)

    username = data.get("username") or "Аноним"
    amount   = data.get("amount", "?")
    currency = data.get("currency", "")
    message  = (data.get("message") or "").strip()

    text = (
        f"💰 <b>Новый донат!</b>\n\n"
        f"👤 От: <b>{username}</b>\n"
        f"💵 Сумма: <b>{amount} {currency}</b>"
    )
    if message:
        text += f"\n💬 Сообщение: {message}"

    try:
        await bot.send_message(ADMIN_ID, text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Не удалось отправить уведомление о донате: {e}")

    return web.Response(status=200)


def create_app(bot: Bot) -> web.Application:
    app = web.Application()
    app.router.add_post("/donation", lambda r: handle_donation(r, bot))
    return app
