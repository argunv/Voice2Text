from aiogram.types import Message
from app.core.redis_client import get_key, set_key


async def handle_error(message: Message):
    user_id = message.from_user.id
    error_key = f"user:{user_id}:errors"

    # Получаем текущее количество ошибок
    error_count = await get_key(error_key)
    error_count = int(error_count) if error_count else 0

    # Увеличиваем счётчик
    error_count += 1
    await set_key(error_key, str(error_count))

    await message.reply(f"Произошла ошибка. Количество ошибок: {error_count}. Попробуйте снова.")