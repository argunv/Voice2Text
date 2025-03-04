import json

import pika

from config.settings import settings


def send_to_queue(data: dict):
    """
    Отправляет сообщение в очередь RabbitMQ.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT)
    )
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE)

    # Сериализуем данные в JSON
    message = json.dumps(data)

    # Отправляем сообщение
    channel.basic_publish(
        exchange='',
        routing_key=settings.RABBITMQ_QUEUE,
        body=message,
    )
    connection.close()
