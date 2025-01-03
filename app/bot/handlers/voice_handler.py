from aiogram.types import Message

from app.core.minio_client import upload_file_to_minio
from app.core.rabbitmq_client import send_to_queue


async def process_voice_message(message: Message):
    voice = message.voice
    file_info = await message.bot.get_file(voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{message.bot.token}/{file_info.file_path}"

    # Сохраняем файл в Minio
    minio_url = upload_file_to_minio(file_url, file_info.file_path)

    # Отправляем задачу на обработку
    task_data = {
        "user_id": message.from_user.id,
        "file_url": minio_url
    }
    send_to_queue(task_data)

    await message.reply("Ваше голосовое сообщение отправлено на обработку.")



async def start_command(message: Message):
    await message.reply("Привет! Отправьте мне голосовое сообщение, и я его расшифрую.")
