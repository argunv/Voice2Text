from aiogram.types import Message

from app.core.minio_client import upload_file_to_minio
from app.core.rabbitmq_client import send_to_queue
from app.core.redis_client import get_key, set_key


async def process_voice_message(message: Message):
    user_id = message.from_user.id
    voice_key = f"user:{user_id}:voice_messages"

    # Получаем текущее количество голосовых сообщений
    voice_count = await get_key(voice_key)
    voice_count = int(voice_count) if voice_count else 0

    # Увеличиваем счётчик
    voice_count += 1
    # NOTE: ttl=3600, чтобы ключ удалялся через час
    # TODO: Стоит вынести ttl в настройки
    await set_key(voice_key, str(voice_count), ttl=3600)

    voice = message.voice
    file_info = await message.bot.get_file(voice.file_id)
    file_url = "https://api.telegram.org/file/bot" + \
              f"{message.bot.token}/{file_info.file_path}"

    # Сохраняем файл в Minio
    minio_url = upload_file_to_minio(file_url, file_info.file_path)

    # Отправляем задачу на обработку
    task_data = {
        "user_id": user_id,
        "file_url": minio_url
    }
    send_to_queue(task_data)

    await message.reply("Ваше голосовое сообщение отправлено на обработку." +
                        f"Количество обработанных сообщений: {voice_count}")

async def start_command(message: Message):
    await message.reply("Привет! Отправьте мне голосовое сообщение, " +
                        "и я его расшифрую.")