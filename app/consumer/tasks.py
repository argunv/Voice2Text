import json

from config.settings import settings
from app.consumer.storage.rabbit import rabbit_connection
from app.consumer.storage.db import save_transcription
from app.core.minio_client import download_file_from_minio
from app.core.transcription_service import transcribe_audio

from app.core.logger import Logger

logger = Logger("rabbitmq_tasks").get_logger()


async def consume_tasks(queue_name: str = None):
    """
    Подключается к RabbitMQ, читает сообщения из очереди в settings.RABBITMQ_QUEUE,
    обрабатывает их (качает файл из MinIO, делает транскрипцию) и сохраняет результат.
    """
    if not queue_name:
        raise ValueError("Variable `queue_name` is None!")
    async with rabbit_connection() as connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(settings.RABBITMQ_QUEUE)

        async for message in queue:
            async with message.process():
                task_data = json.loads(message.body)
                logger.error(f"{message.body}")
                logger.error(f"{message.body}")
                logger.error(f"{task_data}\n\ntask_data['file_url']={task_data['file_url']}")

                file_name = task_data['file_url'].split("/")[-1]
                # Скачиваем файл из MinIO
                local_file = download_file_from_minio(file_name)

                # Выполняем транскрипцию
                transcription = transcribe_audio(local_file)

                # Сохраняем результат в базе данных
                save_transcription(task_data["user_id"], transcription)
