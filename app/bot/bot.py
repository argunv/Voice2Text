import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.types import ContentType
from aiogram.filters import Command
from fastapi import FastAPI

from config.settings import settings
from scripts.ngrok import run_ngrok
from app.bot.handlers.voice_handler import process_voice_message, start_command

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Создание бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

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
        logger.info("Запуск жизненного цикла приложения...")
        # Запуск ngrok и настройка вебхука
        ngrok_url = await run_ngrok()
        webhook_url = f"{ngrok_url}{settings.WEBHOOK_PATH}"
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook установлен: {webhook_url}")
        yield  # Приложение готово к обработке запросов
    except Exception as e:
        logger.error(f"Ошибка в жизненном цикле приложения: {e}")
    finally:
        await bot.delete_webhook()
        logger.info("Webhook удалён.")

def create_app() -> FastAPI:
    """
    Создаёт FastAPI приложение с жизненным циклом и Health Check.
    """
    app = FastAPI(lifespan=lifespan)
    
    @app.get("/")
    async def root():
        """
        Корневой эндпоинт.
        Возвращает статус приложения.
        """
        return {"status": "ok"}

    @app.get("/health")
    async def health():
        """
        Эндпоинт для проверки состояния приложения.
        Возвращает статус "healthy", если приложение работает корректно.
        """
        return {"status": "healthy"}

    return app

async def start_polling():
    """
    Запуск бота в режиме polling.
    Удаляет существующий webhook перед началом опроса.
    """
    logger.info("Запуск бота в режиме polling...")
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    """
    Точка входа в приложение.
    Определяет режим работы: webhook или polling.
    """
    if settings.BOT_MODE == "webhook":
        logger.info("Запуск в режиме webhook")
        uvicorn.run(
            "app.bot.bot:create_app",
            factory=True,
            host="0.0.0.0",
            port=settings.WEBHOOK_PORT,
            log_level="info"
        )
    else:
        logger.info("Запуск в режиме polling")
        asyncio.run(start_polling())
