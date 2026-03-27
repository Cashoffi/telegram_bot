from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from database import (
    get_user_lang,
    get_bug_reports, get_bug_report, set_bug_status, delete_bug_report,
    get_ideas, get_idea, set_idea_status, delete_idea,
)
from keyboards import (
    admin_menu, admin_list_keyboard,
    bug_status_keyboard, idea_status_keyboard,
    delete_confirm_keyboard,
)
from locales import t, t_nested
from utils import send_long

router = Router()

# Уведомление пользователя при смене статуса баг-репорта
BUG_NOTIFY  = {"fixed", "viewed", "in_progress"}
IDEA_NOTIFY = {"accepted", "viewed", "rejected", "implemented", "duplicate"}


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    lang = await get_user_lang(message.from_user.id)
    await message.answer(t(lang, "admin_menu"), reply_markup=admin_menu(lang))


# ── Списки ────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:bugs")
async def admin_show_bugs(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    lang = await get_user_lang(call.from_user.id)
    items = await get_bug_reports()
    if not items:
        await call.message.edit_text(t(lang, "admin_no_items"), reply_markup=admin_menu(lang))
    else:
        await call.message.edit_text(
            t(lang, "admin_bugs"),
            reply_markup=admin_list_keyboard(items, "bug", lang),
        )
    await call.answer()


@router.callback_query(F.data == "admin:ideas")
async def admin_show_ideas(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    lang = await get_user_lang(call.from_user.id)
    items = await get_ideas()
    if not items:
        await call.message.edit_text(t(lang, "admin_no_items"), reply_markup=admin_menu(lang))
    else:
        await call.message.edit_text(
            t(lang, "admin_ideas"),
            reply_markup=admin_list_keyboard(items, "idea", lang),
        )
    await call.answer()


@router.callback_query(F.data == "admin:back")
async def admin_back(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    lang = await get_user_lang(call.from_user.id)
    await call.message.edit_text(t(lang, "admin_menu"), reply_markup=admin_menu(lang))
    await call.answer()


# ── Просмотр конкретного репорта/идеи ────────────────────────────────────────

@router.callback_query(F.data.startswith("view:"))
async def admin_view_item(call: CallbackQuery, bot: Bot):
    if not is_admin(call.from_user.id):
        return
    _, kind, item_id = call.data.split(":")
    item_id = int(item_id)
    lang = await get_user_lang(call.from_user.id)

    if kind == "bug":
        item = await get_bug_report(item_id)
        kb = bug_status_keyboard(item_id, lang)
    else:
        item = await get_idea(item_id)
        kb = idea_status_keyboard(item_id, lang)

    if not item:
        await call.answer("Не найдено")
        return

    status_label = t(lang, f"status_{item['status']}")
    text = (
        f"<b>ID:</b> {item['id']}\n"
        f"<b>Название:</b> {item['title']}\n"
        f"<b>Статус:</b> {status_label}\n"
        f"<b>Дата:</b> {item['created_at']}\n\n"
        f"{item['description']}"
    )

    await call.message.delete()
    await send_long(bot, call.from_user.id, text, parse_mode="HTML")
    await bot.send_message(call.from_user.id, t(lang, "admin_set_status"), reply_markup=kb)

    if item["photo_id"]:
        await bot.send_photo(call.from_user.id, item["photo_id"])

    await call.answer()


# ── Смена статуса ─────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("setstatus:"))
async def admin_set_status(call: CallbackQuery, bot: Bot):
    if not is_admin(call.from_user.id):
        return

    _, kind, item_id, status = call.data.split(":")
    item_id = int(item_id)
    lang = await get_user_lang(call.from_user.id)

    if kind == "bug":
        await set_bug_status(item_id, status)
        item = await get_bug_report(item_id)
    else:
        await set_idea_status(item_id, status)
        item = await get_idea(item_id)

    await call.message.edit_text(t(lang, "admin_status_updated"))
    await call.answer()

    if not item:
        return

    user_id = item["user_id"]
    user_lang = await get_user_lang(user_id)
    section = "notify_bug" if kind == "bug" else "notify_idea"
    notify_text = t_nested(user_lang, section, status, title=item["title"])

    try:
        await bot.send_message(user_id, notify_text, parse_mode="HTML")
    except Exception:
        pass


# ── Удаление ──────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("confirmdelete:"))
async def admin_confirm_delete(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    _, kind, item_id = call.data.split(":")
    item_id = int(item_id)
    lang = await get_user_lang(call.from_user.id)
    await call.message.edit_text(
        t(lang, "admin_confirm_delete"),
        reply_markup=delete_confirm_keyboard(kind, item_id, lang),
    )
    await call.answer()


@router.callback_query(F.data.startswith("dodelete:"))
async def admin_do_delete(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    _, kind, item_id = call.data.split(":")
    item_id = int(item_id)
    lang = await get_user_lang(call.from_user.id)

    if kind == "bug":
        await delete_bug_report(item_id)
    else:
        await delete_idea(item_id)

    await call.message.edit_text(t(lang, "admin_deleted"))
    await call.answer()


@router.callback_query(F.data.startswith("canceldelete:"))
async def admin_cancel_delete(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    _, kind, item_id = call.data.split(":")
    item_id = int(item_id)
    lang = await get_user_lang(call.from_user.id)

    if kind == "bug":
        kb = bug_status_keyboard(item_id, lang)
    else:
        kb = idea_status_keyboard(item_id, lang)

    await call.message.edit_text(t(lang, "admin_set_status"), reply_markup=kb)
    await call.answer()
