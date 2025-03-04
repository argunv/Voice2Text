from aiogram.types import Message

from app.core.minio_client import upload_file_to_minio
from app.core.rabbitmq_client import send_to_queue
from app.core.redis_client import get_key, set_key
from config.settings import settings


async def process_voice_message(message: Message):
    user_id = message.from_user.id
    voice_key = f"user:{user_id}:voice_messages"

    # Получаем текущее количество голосовых сообщений
    voice_count = await get_key(voice_key)
    voice_count = int(voice_count) if voice_count else 0

    # Увеличиваем счётчик
    voice_count += 1

    await set_key(voice_key, str(voice_count), ttl=settings.REDIS_TTL)

    voice = message.voice
    file_info = await message.bot.get_file(voice.file_id)
    file_url = "https://api.telegram.org/file/bot" + \
              f"{message.bot.token}/{file_info.file_path}"

    # Сохраняем файл в Minio
    task_data = upload_file_to_minio(file_url, file_info.file_path)

    task_data['user_id'] = user_id
    send_to_queue(task_data)

    await message.reply("Ваше голосовое сообщение отправлено на обработку." +
                        f"Количество обработанных сообщений: {voice_count}")

async def start_command(message: Message):
    await message.reply("Привет! Отправьте мне голосовое сообщение, " +
                        "и я его расшифрую.")