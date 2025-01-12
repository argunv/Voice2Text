import asyncio

from app.consumer.tasks import consume_tasks


async def main():
    while True:
        await consume_tasks()
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
