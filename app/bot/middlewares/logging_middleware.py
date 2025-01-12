from aiogram.dispatcher.middlewares import BaseMiddleware
from app.core.logger import Logger


logger = Logger("logging_middleware").get_logger()


class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message, data):
        logger.info(f"Received message: {message.text}")
