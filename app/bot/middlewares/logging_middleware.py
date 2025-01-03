import logging

from aiogram.dispatcher.middlewares import BaseMiddleware

logger = logging.getLogger("bot")

class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message, data):
        logger.info(f"Received message: {message.text}")
