import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.types import ContentType, Update
from aiogram.filters import Command
from fastapi import FastAPI, Request

from app.bot import middlewares
from config.settings import settings
from scripts.ngrok import run_ngrok
from app.bot.handlers.voice_handler import process_voice_message, start_command
from app.core.redis_client import get_redis_client
from app.core.logger import Logger

# Настройка логирования
logger = Logger("bot").get_logger()

# Создание бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Регистрация middlewares
middlewares.setup_middlewares(dp=dp)

# Регистрация обработчиков
dp.message.register(start_command, Command(commands=["start"]))
dp.message.register(process_voice_message, lambda message: message.content_type == ContentType.VOICE)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Управление жизненным циклом FastAPI приложения.
    Включает запуск ngrok и настройку Telegram webhook.
    """
    try:
        logger.error("Запуск жизненного цикла приложения...")
        # Инициализация Redis клиента
        await get_redis_client()
        logger.error("Redis клиент инициализирован")

        # Запуск ngrok и настройка вебхука
        ngrok_url = await run_ngrok()
        webhook_url = f"{ngrok_url}{settings.WEBHOOK_PATH}"
        await bot.set_webhook(webhook_url)
        logger.error(f"Webhook установлен: {webhook_url}")
        yield  # Приложение готово к обработке запросов
    except Exception as e:
        logger.error(f"Ошибка в жизненном цикле приложения: {e}")
    finally:
        await bot.delete_webhook()
        logger.error("Webhook удалён.")


def create_app() -> FastAPI:
    """
    Создаёт FastAPI приложение с жизненным циклом и Health Check.
    """
    app = FastAPI(lifespan=lifespan)

    @app.post(settings.WEBHOOK_PATH)
    async def telegram_webhook(request: Request):
        """
        Обработчик вебхуков Telegram.
        """
        try:
            update = Update(**await request.json())
            await dp.feed_update(bot, update)
            return {"status": "ok"}
        except Exception as e:
            logger.error(f"Ошибка обработки webhook: {e}")
            return {"status": "error"}

    @app.get("/")
    async def root():
        return {"status": "ok"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


async def start_polling():
    """
    Запуск бота в режиме polling.
    Удаляет существующий webhook перед началом опроса.
    """
    logger.error("Запуск бота в режиме polling...")
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    """
    Точка входа в приложение.
    Определяет режим работы: webhook или polling.
    """
    if settings.BOT_MODE == "webhook":
        logger.error("Запуск в режиме webhook")
        uvicorn.run(
            "app.bot.bot:create_app",
            factory=True,
            host="0.0.0.0",
            port=settings.WEBHOOK_PORT,
            log_level="error"
        )
    else:
        logger.error("Запуск в режиме polling")
        asyncio.run(start_polling())
