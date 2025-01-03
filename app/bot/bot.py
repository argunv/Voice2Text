import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import ContentType, Message

from app.bot.handlers.voice_handler import process_voice_message, start_command
from config.settings import settings

# Создаем экземпляры бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Регистрация обработчика команды /start
dp.message.register(
    start_command,
    Command(commands=["start"]),
)

# Регистрация обработчика голосовых сообщений
dp.message.register(
    process_voice_message,
    lambda message: message.content_type == ContentType.VOICE,
)

async def main():
    # Установка команд для бота
    await bot.set_my_commands([
        {"command": "start", "description": "Начать работу с ботом"}
    ])

    # Запуск обработчиков
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
