TEXTS = {
    "ru": {
        "choose_language":       "Выберите язык / Choose language:",
        "language_set":          "Язык установлен: Русский 🇷🇺",
        "main_menu":             "Главное меню",
        "btn_bug_report":        "🐛 Баг-репорт",
        "btn_suggest_idea":      "💡 Предложить идею",
        "btn_change_lang":       "🌐 Сменить язык",
        "btn_profile":           "👤 Личный кабинет",
        "btn_lists":             "📋 Списки",
        "btn_admin_panel":       "⚙️ Админ-панель",

        # Bug report flow
        "bug_title":             "Введите краткое название бага:",
        "bug_description":       "Опишите баг подробно (можно несколько сообщений — отправьте /done когда закончите):",
        "bug_screenshot":        "Прикрепите скриншот (или нажмите «Пропустить»):",
        "bug_skip":              "Пропустить",
        "bug_sent":              "✅ Баг-репорт отправлен! Мы рассмотрим его в ближайшее время.",
        "bug_confirm":           "📋 Ваш баг-репорт:\n\n<b>Название:</b> {title}\n\n<b>Описание:</b>\n{description}\n\nВсё верно?",

        # Idea flow
        "idea_title":            "Введите краткое название идеи:",
        "idea_description":      "Опишите идею подробно (можно несколько сообщений — отправьте /done когда закончите):",
        "idea_screenshot":       "Прикрепите изображение к идее (или нажмите «Пропустить»):",
        "idea_sent":             "✅ Идея отправлена! Спасибо за ваш вклад.",
        "idea_confirm":          "📋 Ваша идея:\n\n<b>Название:</b> {title}\n\n<b>Описание:</b>\n{description}\n\nВсё верно?",

        "btn_confirm":           "✅ Подтвердить",
        "btn_cancel":            "❌ Отмена",
        "cancelled":             "Отменено. Возврат в главное меню.",
        "done_hint":             "Отправьте /done чтобы завершить ввод описания.",
        "karma_earned":          "⭐ +1 карма за баг-репорт!",

        # Profile
        "profile_text":          "👤 <b>Личный кабинет</b>\n\nБаг-репортов отправлено: <b>{bugs}</b>\nИдей предложено: <b>{ideas}</b>\nКарма: <b>{karma} ⭐</b>",

        # Public lists
        "lists_menu":            "Выберите список:",
        "lists_bugs_all":        "🐛 Все баг-репорты",
        "lists_bugs_fixed":      "✅ Исправленные",
        "lists_ideas_all":       "💡 Все идеи",
        "lists_ideas_done":      "🚀 Реализованные",
        "list_empty":            "Список пуст.",
        "pub_view_back":         "◀️ Назад к списку",
        "pub_has_screenshot":    "📷 К этому элементу прикреплён скриншот.",

        # Notifications to user
        "notify_bug": {
            "fixed":       "✅ Ваш баг-репорт <b>«{title}»</b> помечен как <b>Исправлено</b>.",
            "viewed":      "👁 Ваш баг-репорт <b>«{title}»</b> <b>просмотрен</b>.",
            "in_progress": "🔧 Ваш баг-репорт <b>«{title}»</b> — <b>в процессе исправления</b>.",
        },
        "notify_idea": {
            "accepted":    "✅ Ваша идея <b>«{title}»</b> <b>принята</b>!",
            "viewed":      "👁 Ваша идея <b>«{title}»</b> <b>просмотрена</b>.",
            "rejected":    "❌ Ваша идея <b>«{title}»</b> <b>отклонена</b>.",
            "implemented": "🚀 Ваша идея <b>«{title}»</b> <b>реализована</b>!",
            "duplicate":   "♻️ Ваша идея <b>«{title}»</b> — <b>уже была реализована ранее</b>.",
        },

        # Admin panel
        "admin_menu":            "⚙️ Панель администратора",
        "admin_bugs":            "🐛 Баг-репорты",
        "admin_ideas":           "💡 Идеи",
        "admin_no_items":        "Пусто.",
        "admin_set_status":      "Установить статус:",
        "admin_back":            "◀️ Назад",
        "admin_status_updated":  "Статус обновлён.",
        "admin_delete":          "🗑 Удалить",
        "admin_confirm_delete":  "⚠️ Удалить этот элемент? Действие необратимо.",
        "admin_deleted":         "✅ Элемент удалён.",
        "btn_yes_delete":        "✅ Да, удалить",
        "btn_no_delete":         "❌ Отмена",

        # Statuses display
        "status_fixed":          "Исправлено",
        "status_viewed":         "Просмотрено",
        "status_in_progress":    "В процессе",
        "status_accepted":       "Принята",
        "status_rejected":       "Отклонена",
        "status_implemented":    "Реализована",
        "status_duplicate":      "Уже реализована",
        "status_new":            "Новый",
    },

    "en": {
        "choose_language":       "Выберите язык / Choose language:",
        "language_set":          "Language set: English 🇬🇧",
        "main_menu":             "Main menu",
        "btn_bug_report":        "🐛 Bug Report",
        "btn_suggest_idea":      "💡 Suggest Idea",
        "btn_change_lang":       "🌐 Change language",
        "btn_profile":           "👤 My Profile",
        "btn_lists":             "📋 Lists",
        "btn_admin_panel":       "⚙️ Admin Panel",

        "bug_title":             "Enter a short bug title:",
        "bug_description":       "Describe the bug in detail (you can send multiple messages — send /done when finished):",
        "bug_screenshot":        "Attach a screenshot (or press «Skip»):",
        "bug_skip":              "Skip",
        "bug_sent":              "✅ Bug report submitted! We'll review it soon.",
        "bug_confirm":           "📋 Your bug report:\n\n<b>Title:</b> {title}\n\n<b>Description:</b>\n{description}\n\nLooks good?",

        "idea_title":            "Enter a short idea title:",
        "idea_description":      "Describe your idea in detail (you can send multiple messages — send /done when finished):",
        "idea_screenshot":       "Attach an image (or press «Skip»):",
        "idea_sent":             "✅ Idea submitted! Thanks for your contribution.",
        "idea_confirm":          "📋 Your idea:\n\n<b>Title:</b> {title}\n\n<b>Description:</b>\n{description}\n\nLooks good?",

        "btn_confirm":           "✅ Confirm",
        "btn_cancel":            "❌ Cancel",
        "cancelled":             "Cancelled. Back to main menu.",
        "done_hint":             "Send /done to finish entering the description.",
        "karma_earned":          "⭐ +1 karma for bug report!",

        # Profile
        "profile_text":          "👤 <b>My Profile</b>\n\nBug reports sent: <b>{bugs}</b>\nIdeas suggested: <b>{ideas}</b>\nKarma: <b>{karma} ⭐</b>",

        # Public lists
        "lists_menu":            "Choose a list:",
        "lists_bugs_all":        "🐛 All Bug Reports",
        "lists_bugs_fixed":      "✅ Fixed Bugs",
        "lists_ideas_all":       "💡 All Ideas",
        "lists_ideas_done":      "🚀 Implemented Ideas",
        "list_empty":            "Nothing here.",
        "pub_view_back":         "◀️ Back to list",
        "pub_has_screenshot":    "📷 This item has a screenshot attached.",

        "notify_bug": {
            "fixed":       "✅ Your bug report <b>«{title}»</b> has been marked as <b>Fixed</b>.",
            "viewed":      "👁 Your bug report <b>«{title}»</b> has been <b>viewed</b>.",
            "in_progress": "🔧 Your bug report <b>«{title}»</b> is <b>in progress</b>.",
        },
        "notify_idea": {
            "accepted":    "✅ Your idea <b>«{title}»</b> has been <b>accepted</b>!",
            "viewed":      "👁 Your idea <b>«{title}»</b> has been <b>viewed</b>.",
            "rejected":    "❌ Your idea <b>«{title}»</b> has been <b>rejected</b>.",
            "implemented": "🚀 Your idea <b>«{title}»</b> has been <b>implemented</b>!",
            "duplicate":   "♻️ Your idea <b>«{title}»</b> — <b>was already implemented before</b>.",
        },

        "admin_menu":            "⚙️ Admin panel",
        "admin_bugs":            "🐛 Bug Reports",
        "admin_ideas":           "💡 Ideas",
        "admin_no_items":        "Nothing here.",
        "admin_set_status":      "Set status:",
        "admin_back":            "◀️ Back",
        "admin_status_updated":  "Status updated.",
        "admin_delete":          "🗑 Delete",
        "admin_confirm_delete":  "⚠️ Delete this item? This cannot be undone.",
        "admin_deleted":         "✅ Item deleted.",
        "btn_yes_delete":        "✅ Yes, delete",
        "btn_no_delete":         "❌ Cancel",

        "status_fixed":          "Fixed",
        "status_viewed":         "Viewed",
        "status_in_progress":    "In progress",
        "status_accepted":       "Accepted",
        "status_rejected":       "Rejected",
        "status_implemented":    "Implemented",
        "status_duplicate":      "Already implemented",
        "status_new":            "New",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Получить текст по ключу с подстановкой переменных."""
    lang = lang if lang in TEXTS else "ru"
    val = TEXTS[lang].get(key, key)
    if isinstance(val, dict):
        return val
    return val.format(**kwargs) if kwargs else val


def t_nested(lang: str, section: str, key: str, **kwargs) -> str:
    """Получить вложенный текст (например notify_bug → fixed)."""
    lang = lang if lang in TEXTS else "ru"
    val = TEXTS[lang].get(section, {}).get(key, key)
    return val.format(**kwargs) if kwargs else val
