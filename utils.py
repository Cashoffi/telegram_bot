from aiogram import Bot

MAX_MSG_LEN = 4096


async def send_long(bot: Bot, chat_id: int, text: str, **kwargs):
    """Отправляет длинное сообщение, разбивая на части по MAX_MSG_LEN символов."""
    while len(text) > MAX_MSG_LEN:
        # Разрезаем по последнему переносу строки в пределах лимита
        cut = text.rfind("\n", 0, MAX_MSG_LEN)
        if cut == -1:
            cut = MAX_MSG_LEN
        await bot.send_message(chat_id, text[:cut], **kwargs)
        text = text[cut:].lstrip("\n")
        # kwargs с parse_mode только для первого куска, остальные без разметки
        kwargs.pop("reply_markup", None)
    if text.strip():
        await bot.send_message(chat_id, text, **kwargs)


def format_report(item, kind: str, lang_t) -> str:
    """Форматирует запись репорта/идеи для отображения админу."""
    status_key = f"status_{item['status']}"
    lines = [
        f"<b>ID:</b> {item['id']}",
        f"<b>{'Название' if kind == 'ru' else 'Title'}:</b> {item['title']}",
        f"<b>{'Статус' if kind == 'ru' else 'Status'}:</b> {lang_t(status_key)}",
        f"<b>{'Дата' if kind == 'ru' else 'Date'}:</b> {item['created_at']}",
        "",
        item['description'],
    ]
    return "\n".join(lines)
