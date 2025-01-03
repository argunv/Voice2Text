from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    awaiting_voice = State()       # Ожидание голосового сообщения
    processing_voice = State()    # Обработка голосового сообщения
    awaiting_confirmation = State()  # Ожидание подтверждения пользователя
