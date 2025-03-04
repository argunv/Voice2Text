from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.core.logger import Logger


logger = Logger("middleware_logging").get_logger()


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Логируем текст сообщения
        logger.info(f"Received message: {event.text}")
        # Передаём управление дальше по цепочке
        return await handler(event, data)
