from aio_pika import Message, connect_robust
from contextlib import asynccontextmanager

from config.settings import settings


@asynccontextmanager
async def rabbit_connection():
    """
    Асинхронный контекст-менеджер, который создаёт и закрывает подключение к RabbitMQ.
    """
    connection_url = "amqp://%s:%s@%s/" % (
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASS,
        settings.RABBITMQ_HOST
    )
    connection = await connect_robust(connection_url)
    try:
        yield connection
    finally:
        await connection.close()


async def send_message_to_queue(message_body: str, queue_name: str):
    """
    Отправляет сообщение в указанную очередь RabbitMQ.
    """
    async with rabbit_connection() as connection:
        channel = await connection.channel()
        # Объявим очередь (если она не существует, она будет создана)
        queue = await channel.declare_queue(queue_name)
        # Публикуем сообщение в обменник по routing_key, который равен имени очереди
        await channel.default_exchange.publish(
            Message(body=message_body.encode()),
            routing_key=queue_name
        )
