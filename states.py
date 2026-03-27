from aiogram.fsm.state import State, StatesGroup


class BugReport(StatesGroup):
    title       = State()
    description = State()
    screenshot  = State()
    confirm     = State()


class Idea(StatesGroup):
    title       = State()
    description = State()
    screenshot  = State()
    confirm     = State()
