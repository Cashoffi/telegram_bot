from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from database import get_user_lang, add_bug_report, add_karma
from keyboards import cancel_keyboard, skip_keyboard, confirm_keyboard, main_menu
from locales import t
from states import BugReport
from utils import send_long

router = Router()


@router.message(F.text.in_(["🐛 Баг-репорт", "🐛 Bug Report"]))
async def start_bug_report(message: Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    await state.set_state(BugReport.title)
    await message.answer(t(lang, "bug_title"), reply_markup=cancel_keyboard(lang))


@router.message(BugReport.title)
async def bug_title(message: Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    await state.update_data(title=message.text.strip(), description_parts=[])
    await state.set_state(BugReport.description)
    await message.answer(t(lang, "bug_description"), reply_markup=cancel_keyboard(lang))
    await message.answer(t(lang, "done_hint"))


@router.message(BugReport.description, F.text == "/done")
async def bug_description_done(message: Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    data = await state.get_data()
    parts = data.get("description_parts", [])
    if not parts:
        await message.answer(t(lang, "bug_description"))
        return
    await state.set_state(BugReport.screenshot)
    await message.answer(t(lang, "bug_screenshot"), reply_markup=skip_keyboard(lang))


@router.message(BugReport.description)
async def bug_description_part(message: Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    data = await state.get_data()
    parts = data.get("description_parts", [])
    parts.append(message.text or "")
    await state.update_data(description_parts=parts)
    await message.answer(t(lang, "done_hint"))


@router.message(BugReport.screenshot, F.photo)
async def bug_screenshot_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await _show_bug_confirm(message, state)


@router.callback_query(F.data == "skip_photo", BugReport.screenshot)
async def bug_screenshot_skip(call: CallbackQuery, state: FSMContext):
    await state.update_data(photo_id=None)
    await call.message.delete()
    await _show_bug_confirm(call.message, state, user_id=call.from_user.id)
    await call.answer()


async def _show_bug_confirm(message: Message, state: FSMContext, user_id: int | None = None):
    uid = user_id or message.from_user.id
    lang = await get_user_lang(uid)
    data = await state.get_data()
    description = "\n".join(data.get("description_parts", []))
    preview = (description[:300] + "...") if len(description) > 300 else description
    text = t(lang, "bug_confirm", title=data["title"], description=preview)
    await state.set_state(BugReport.confirm)
    await state.update_data(description=description)
    await message.answer(text, parse_mode="HTML", reply_markup=confirm_keyboard(lang))


@router.callback_query(F.data == "confirm", BugReport.confirm)
async def bug_confirm(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = await get_user_lang(call.from_user.id)
    data = await state.get_data()
    await state.clear()

    report_id = await add_bug_report(
        user_id=call.from_user.id,
        title=data["title"],
        description=data["description"],
        photo_id=data.get("photo_id"),
    )
    await add_karma(call.from_user.id)

    # Уведомление администратору
    user = call.from_user
    admin_text = (
        f"🐛 <b>Новый баг-репорт #{report_id}</b>\n"
        f"От: {user.full_name} (@{user.username or '—'}, ID: {user.id})\n\n"
        f"<b>Название:</b> {data['title']}\n\n"
        f"<b>Описание:</b>\n{data['description']}"
    )
    await send_long(bot, ADMIN_ID, admin_text, parse_mode="HTML")
    if data.get("photo_id"):
        await bot.send_photo(ADMIN_ID, data["photo_id"], caption=f"Скриншот к репорту #{report_id}")

    await call.message.delete()
    await call.message.answer(t(lang, "bug_sent"), reply_markup=main_menu(lang, is_admin=call.from_user.id == ADMIN_ID))
    await call.message.answer(t(lang, "karma_earned"))
    await call.answer()
