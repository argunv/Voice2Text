import json

from aio_pika import Message, connect_robust

from app.consumer.storage.db import save_transcription
from app.core.minio_client import download_file_from_minio
from app.core.transcription_service import transcribe_audio


async def consume_tasks():
    connection = await connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    queue = await channel.declare_queue("voice_tasks")

    async for message in queue:
        async with message.process():
            task_data = json.loads(message.body)

            # Скачиваем файл из Minio
            local_file = download_file_from_minio(task_data["file_url"])

            # Выполняем транскрипцию
            transcription = transcribe_audio(local_file)

            # Сохраняем результат в базе данных
            save_transcription(task_data["user_id"], transcription)
