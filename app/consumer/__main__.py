import asyncio

from app.consumer.tasks import consume_tasks
from config.settings import settings


async def main():
    while True:
        await consume_tasks(settings.RABBITMQ_QUEUE)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
