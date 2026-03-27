import aiosqlite
from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id   INTEGER PRIMARY KEY,
                lang      TEXT    NOT NULL DEFAULT 'ru',
                karma     INTEGER NOT NULL DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bug_reports (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                title       TEXT    NOT NULL,
                description TEXT    NOT NULL,
                photo_id    TEXT,
                status      TEXT    NOT NULL DEFAULT 'new',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                title       TEXT    NOT NULL,
                description TEXT    NOT NULL,
                photo_id    TEXT,
                status      TEXT    NOT NULL DEFAULT 'new',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
        # Migration: add karma column if not exists (for existing DBs)
        try:
            await db.execute("ALTER TABLE users ADD COLUMN karma INTEGER NOT NULL DEFAULT 0")
            await db.commit()
        except Exception:
            pass


# ── Users ────────────────────────────────────────────────────────────────────

async def get_user_lang(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT lang FROM users WHERE user_id = ?", (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else "ru"


async def set_user_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (user_id, lang) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET lang = excluded.lang",
            (user_id, lang),
        )
        await db.commit()


async def add_karma(user_id: int, amount: int = 1):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (user_id, karma) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET karma = karma + ?",
            (user_id, amount, amount),
        )
        await db.commit()


async def get_user_stats(user_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM bug_reports WHERE user_id = ?", (user_id,)
        ) as cur:
            bugs = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT COUNT(*) FROM ideas WHERE user_id = ?", (user_id,)
        ) as cur:
            ideas = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT karma FROM users WHERE user_id = ?", (user_id,)
        ) as cur:
            row = await cur.fetchone()
            karma = row[0] if row else 0
    return {"bugs": bugs, "ideas": ideas, "karma": karma}


# ── Bug reports ───────────────────────────────────────────────────────────────

async def add_bug_report(user_id: int, title: str, description: str, photo_id: str | None) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO bug_reports (user_id, title, description, photo_id) VALUES (?, ?, ?, ?)",
            (user_id, title, description, photo_id),
        )
        await db.commit()
        return cur.lastrowid


async def get_bug_reports(status: str | None = None):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if status:
            async with db.execute(
                "SELECT * FROM bug_reports WHERE status = ? ORDER BY created_at DESC", (status,)
            ) as cur:
                return await cur.fetchall()
        else:
            async with db.execute(
                "SELECT * FROM bug_reports ORDER BY created_at DESC"
            ) as cur:
                return await cur.fetchall()


async def get_bug_report(report_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM bug_reports WHERE id = ?", (report_id,)
        ) as cur:
            return await cur.fetchone()


async def set_bug_status(report_id: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE bug_reports SET status = ? WHERE id = ?", (status, report_id)
        )
        await db.commit()


async def delete_bug_report(report_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM bug_reports WHERE id = ?", (report_id,))
        await db.commit()


# ── Ideas ─────────────────────────────────────────────────────────────────────

async def add_idea(user_id: int, title: str, description: str, photo_id: str | None) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO ideas (user_id, title, description, photo_id) VALUES (?, ?, ?, ?)",
            (user_id, title, description, photo_id),
        )
        await db.commit()
        return cur.lastrowid


async def get_ideas(status: str | None = None):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if status:
            async with db.execute(
                "SELECT * FROM ideas WHERE status = ? ORDER BY created_at DESC", (status,)
            ) as cur:
                return await cur.fetchall()
        else:
            async with db.execute(
                "SELECT * FROM ideas ORDER BY created_at DESC"
            ) as cur:
                return await cur.fetchall()


async def get_idea(idea_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM ideas WHERE id = ?", (idea_id,)
        ) as cur:
            return await cur.fetchone()


async def set_idea_status(idea_id: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE ideas SET status = ? WHERE id = ?", (status, idea_id)
        )
        await db.commit()


async def delete_idea(idea_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
        await db.commit()
