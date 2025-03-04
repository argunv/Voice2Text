from aiogram import BaseMiddleware, exceptions
from aiogram.types import Message
from app.core.logger import Logger


logger = Logger("middleware_error_handler").get_logger()


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(
                f"Error occurred while processing message '{event.text}': {e}"
            )
            # Сообщить пользователю об ошибке
            await event.answer(
                "Произошла ошибка при обработке вашего запроса."
            )
