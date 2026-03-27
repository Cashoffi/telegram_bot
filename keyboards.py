from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from locales import t


def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
        ]
    ])


def main_menu(lang: str, is_admin: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=t(lang, "btn_bug_report")), KeyboardButton(text=t(lang, "btn_suggest_idea"))],
        [KeyboardButton(text=t(lang, "btn_lists"))],
        [KeyboardButton(text=t(lang, "btn_profile")), KeyboardButton(text=t(lang, "btn_change_lang"))],
    ]
    if is_admin:
        keyboard.append([KeyboardButton(text=t(lang, "btn_admin_panel"))])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def skip_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "bug_skip"), callback_data="skip_photo")],
        [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="cancel")],
    ])


def confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(lang, "btn_confirm"), callback_data="confirm"),
            InlineKeyboardButton(text=t(lang, "btn_cancel"),  callback_data="cancel"),
        ]
    ])


def cancel_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="cancel")]
    ])


# ── Public lists keyboards ────────────────────────────────────────────────────

def lists_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(lang, "lists_bugs_all"),   callback_data="lists:bugs:all"),
            InlineKeyboardButton(text=t(lang, "lists_bugs_fixed"),  callback_data="lists:bugs:fixed"),
        ],
        [
            InlineKeyboardButton(text=t(lang, "lists_ideas_all"),  callback_data="lists:ideas:all"),
            InlineKeyboardButton(text=t(lang, "lists_ideas_done"), callback_data="lists:ideas:implemented"),
        ],
    ])


def public_list_keyboard(items: list, item_type: str, list_type: str, lang: str) -> InlineKeyboardMarkup:
    buttons = []
    for item in items:
        status_label = t(lang, f"status_{item['status']}")
        label = f"[{item['id']}] {item['title'][:28]} — {status_label}"
        buttons.append([
            InlineKeyboardButton(
                text=label,
                callback_data=f"pubview:{item_type}:{item['id']}:{list_type}"
            )
        ])
    buttons.append([InlineKeyboardButton(text=t(lang, "admin_back"), callback_data="lists:menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def public_item_keyboard(item_type: str, list_type: str, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t(lang, "pub_view_back"),
            callback_data=f"lists:{item_type}:{list_type}"
        )]
    ])


# ── Admin keyboards ───────────────────────────────────────────────────────────

def admin_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "admin_bugs"),  callback_data="admin:bugs")],
        [InlineKeyboardButton(text=t(lang, "admin_ideas"), callback_data="admin:ideas")],
    ])


def admin_list_keyboard(items: list, item_type: str, lang: str) -> InlineKeyboardMarkup:
    buttons = []
    for item in items:
        status_key = f"status_{item['status']}"
        status_label = t(lang, status_key)
        label = f"[{item['id']}] {item['title'][:30]} — {status_label}"
        buttons.append([
            InlineKeyboardButton(text=label, callback_data=f"view:{item_type}:{item['id']}")
        ])
    buttons.append([InlineKeyboardButton(text=t(lang, "admin_back"), callback_data="admin:back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def bug_status_keyboard(report_id: int, lang: str) -> InlineKeyboardMarkup:
    statuses = [
        ("viewed",      t(lang, "status_viewed")),
        ("in_progress", t(lang, "status_in_progress")),
        ("fixed",       t(lang, "status_fixed")),
    ]
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"setstatus:bug:{report_id}:{key}")]
        for key, label in statuses
    ]
    buttons.append([InlineKeyboardButton(text=t(lang, "admin_delete"), callback_data=f"confirmdelete:bug:{report_id}")])
    buttons.append([InlineKeyboardButton(text=t(lang, "admin_back"), callback_data="admin:bugs")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def idea_status_keyboard(idea_id: int, lang: str) -> InlineKeyboardMarkup:
    statuses = [
        ("viewed",      t(lang, "status_viewed")),
        ("accepted",    t(lang, "status_accepted")),
        ("rejected",    t(lang, "status_rejected")),
        ("implemented", t(lang, "status_implemented")),
        ("duplicate",   t(lang, "status_duplicate")),
    ]
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"setstatus:idea:{idea_id}:{key}")]
        for key, label in statuses
    ]
    buttons.append([InlineKeyboardButton(text=t(lang, "admin_delete"), callback_data=f"confirmdelete:idea:{idea_id}")])
    buttons.append([InlineKeyboardButton(text=t(lang, "admin_back"), callback_data="admin:ideas")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def delete_confirm_keyboard(kind: str, item_id: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_yes_delete"), callback_data=f"dodelete:{kind}:{item_id}")],
        [InlineKeyboardButton(text=t(lang, "btn_no_delete"),  callback_data=f"canceldelete:{kind}:{item_id}")],
    ])
