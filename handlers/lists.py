from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from database import get_user_lang, get_bug_reports, get_ideas, get_bug_report, get_idea
from keyboards import lists_keyboard, public_list_keyboard, public_item_keyboard
from locales import t

router = Router()

# Mapping: list_type → status filter (None = all)
_BUG_FILTERS  = {"all": None, "fixed": "fixed"}
_IDEA_FILTERS = {"all": None, "implemented": "implemented"}


async def _safe_edit(call: CallbackQuery, text: str, reply_markup=None, parse_mode: str | None = None):
    """Edit message, ignoring 'message is not modified' errors."""
    try:
        await call.message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@router.callback_query(F.data == "lists:menu")
async def lists_back_to_menu(call: CallbackQuery):
    lang = await get_user_lang(call.from_user.id)
    await _safe_edit(call, t(lang, "lists_menu"), reply_markup=lists_keyboard(lang))
    await call.answer()


@router.callback_query(F.data.startswith("lists:bugs:"))
async def lists_bugs(call: CallbackQuery):
    lang = await get_user_lang(call.from_user.id)
    list_type = call.data.split(":")[2]  # all | fixed
    status = _BUG_FILTERS.get(list_type)
    items = await get_bug_reports(status=status)
    if not items:
        await _safe_edit(call, t(lang, "list_empty"), reply_markup=lists_keyboard(lang))
    else:
        title = t(lang, "lists_bugs_fixed" if list_type == "fixed" else "lists_bugs_all")
        await _safe_edit(call, title, reply_markup=public_list_keyboard(items, "bugs", list_type, lang))
    await call.answer()


@router.callback_query(F.data.startswith("lists:ideas:"))
async def lists_ideas(call: CallbackQuery):
    lang = await get_user_lang(call.from_user.id)
    list_type = call.data.split(":")[2]  # all | implemented
    status = _IDEA_FILTERS.get(list_type)
    items = await get_ideas(status=status)
    if not items:
        await _safe_edit(call, t(lang, "list_empty"), reply_markup=lists_keyboard(lang))
    else:
        title = t(lang, "lists_ideas_done" if list_type == "implemented" else "lists_ideas_all")
        await _safe_edit(call, title, reply_markup=public_list_keyboard(items, "ideas", list_type, lang))
    await call.answer()


@router.callback_query(F.data.startswith("pubview:"))
async def public_view_item(call: CallbackQuery):
    _, item_type, item_id_str, list_type = call.data.split(":")
    item_id = int(item_id_str)
    lang = await get_user_lang(call.from_user.id)

    if item_type == "bugs":
        item = await get_bug_report(item_id)
    else:
        item = await get_idea(item_id)

    if not item:
        await call.answer("Не найдено / Not found")
        return

    status_label = t(lang, f"status_{item['status']}")
    text = (
        f"<b>#{item['id']} {item['title']}</b>\n"
        f"<b>Статус / Status:</b> {status_label}\n"
        f"<b>Дата / Date:</b> {item['created_at']}\n\n"
        f"{item['description']}"
    )
    if item["photo_id"]:
        text += f"\n\n{t(lang, 'pub_has_screenshot')}"

    if len(text) > 4096:
        text = text[:4090] + "..."

    await _safe_edit(call, text, parse_mode="HTML", reply_markup=public_item_keyboard(item_type, list_type, lang))
    await call.answer()
