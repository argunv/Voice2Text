from unittest.mock import AsyncMock

from aiogram.types import Message

from app.bot.handlers.voice_handler import process_voice_message


async def test_process_voice_message():
    mock_message = AsyncMock(spec=Message)
    mock_message.voice = AsyncMock(file_id="test_file_id")
    mock_message.reply = AsyncMock()

    await process_voice_message(mock_message)

    mock_message.reply.assert_called_once_with("Ваше голосовое сообщение отправлено на обработку.")
