import json

import pika

from config.settings import settings


def test_rabbitmq_send_receive():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT)
    )
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE)

    test_message = {"user_id": 1, "file_url": "http://example.com/test_audio.mp3"}
    channel.basic_publish(exchange="", routing_key=settings.RABBITMQ_QUEUE, body=json.dumps(test_message))

    method_frame, header_frame, body = channel.basic_get(queue=settings.RABBITMQ_QUEUE, auto_ack=True)
    received_message = json.loads(body)

    assert received_message == test_message
    connection.close()
