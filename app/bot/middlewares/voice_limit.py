from aiogram import BaseMiddleware
from aiogram.types import Message

from config.settings import settings
from app.core.logger import Logger


logger = Logger("middleware_voice_limit").get_logger()


class VoiceLimitMiddleware(BaseMiddleware):
    """
    Middleware, которое ограничивает длительность и/или размер голосового сообщения,
    используя настройки из config/settings.
    """

    async def __call__(self, handler, event: Message, data: dict):
        # Проверяем, является ли сообщение голосовым
        if event.voice:
            duration = event.voice.duration  # В секундах
            size = event.voice.file_size     # В байтах

            max_duration = settings.MAX_VOICE_DURATION
            max_size = settings.MAX_VOICE_SIZE

            # Проверяем длительность
            if duration > max_duration:
                logger.info(f"Voice message too long: {duration} sec > {max_duration} sec")
                await event.answer(
                    f"Слишком длинное голосовое сообщение. Максимальная допустимая длительность: {max_duration} сек."
                )
                return  # Прерываем цепочку, хендлеры не вызываются

            # Проверяем размер
            if size > max_size:
                logger.info(f"Voice message too big: {size} bytes > {max_size} bytes")
                await event.answer(
                    f"Файл голосового сообщения слишком большой. Максимально допустимый размер: {max_size} байт."
                )
                return

        # Если всё ок, передаём дальше
        return await handler(event, data)
