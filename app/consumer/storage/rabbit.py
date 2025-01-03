from aio_pika import Message, connect_robust


async def get_rabbit_connection():
    """
    Создает устойчивое соединение с RabbitMQ.
    """
    return await connect_robust("amqp://guest:guest@rabbitmq/")

async def send_message_to_queue(message_body, queue_name):
    """
    Отправляет сообщение в очередь.
    """
    connection = await get_rabbit_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key=queue_name
    )
    await connection.close()
