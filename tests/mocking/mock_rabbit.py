from unittest.mock import patch


class MockRabbitMQChannel:
    def queue_declare(self, queue):
        print(f"Mock queue declare: {queue}")
        return True

    def basic_publish(self, exchange, routing_key, body):
        print(f"Mock publish: {body} to {routing_key}")
        return True

class MockRabbitMQConnection:
    def channel(self):
        return MockRabbitMQChannel()

@patch("app.core.rabbitmq_client.pika.BlockingConnection", return_value=MockRabbitMQConnection())
def mock_rabbitmq_connection(func):
    return func
