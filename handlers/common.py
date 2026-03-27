from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from database import get_user_lang, set_user_lang, get_user_stats
from keyboards import lang_keyboard, main_menu, lists_keyboard, admin_menu
from locales import t

router = Router()


def _is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_lang(message.from_user.id)
    await message.answer(
        t(lang, "choose_language"),
        reply_markup=lang_keyboard(),
    )


@router.callback_query(F.data.startswith("lang:"))
async def set_language(call: CallbackQuery, state: FSMContext):
    lang = call.data.split(":")[1]
    await set_user_lang(call.from_user.id, lang)
    await call.message.delete()
    await call.message.answer(
        t(lang, "language_set"),
        reply_markup=main_menu(lang, is_admin=_is_admin(call.from_user.id)),
    )
    await call.answer()


@router.message(F.text.in_(["🌐 Сменить язык", "🌐 Change language"]))
async def change_language(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_lang(message.from_user.id)
    await message.answer(
        t(lang, "choose_language"),
        reply_markup=lang_keyboard(),
    )


@router.callback_query(F.data == "cancel")
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await get_user_lang(call.from_user.id)
    await call.message.delete()
    await call.message.answer(
        t(lang, "cancelled"),
        reply_markup=main_menu(lang, is_admin=_is_admin(call.from_user.id)),
    )
    await call.answer()


# ── Profile ───────────────────────────────────────────────────────────────────

@router.message(F.text.in_(["👤 Личный кабинет", "👤 My Profile"]))
async def show_profile(message: Message):
    lang = await get_user_lang(message.from_user.id)
    stats = await get_user_stats(message.from_user.id)
    await message.answer(
        t(lang, "profile_text", bugs=stats["bugs"], ideas=stats["ideas"], karma=stats["karma"]),
        parse_mode="HTML",
    )


# ── Public lists ──────────────────────────────────────────────────────────────

@router.message(F.text.in_(["📋 Списки", "📋 Lists"]))
async def show_lists_menu(message: Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(t(lang, "lists_menu"), reply_markup=lists_keyboard(lang))


# ── Admin panel button ────────────────────────────────────────────────────────

@router.message(F.text.in_(["⚙️ Админ-панель", "⚙️ Admin Panel"]))
async def admin_panel_button(message: Message):
    if not _is_admin(message.from_user.id):
        return
    lang = await get_user_lang(message.from_user.id)
    await message.answer(t(lang, "admin_menu"), reply_markup=admin_menu(lang))
