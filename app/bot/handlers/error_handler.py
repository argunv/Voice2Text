from aiogram.types import Message


async def handle_error(message: Message):
    await message.reply("Произошла ошибка. Пожалуйста, попробуйте снова позже.")
