from aiogram import Dispatcher

from .logging import LoggingMiddleware
from .error_handler import ErrorHandlerMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    """
    Регистрируем все middlewares в диспетчере.
    """
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ErrorHandlerMiddleware())
