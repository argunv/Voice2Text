import asyncio

from app.consumer.tasks import consume_tasks


async def main():
    await consume_tasks()

if __name__ == "__main__":
    asyncio.run(main())
