from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Bot
from app.send import send_vacancies

router=Router()

async def send_and_dispatch(bot: Bot):
    msg = await send_vacancies()
    await bot.send_message(
        chat_id=???????????,
        text=msg,
        parse_mode="HTML",
        message_thread_id=2
    )
    
@router.message(Command("chat_id"))
async def debug_info(message: Message):
    info = (
        f"Chat ID: {message.chat.id}\n"
        f"Chat Type: {message.chat.type}\n"
        f"Thread ID: {message.message_thread_id}\n"
        f"Is Topic Message: {message.is_topic_message}"
    )
    await message.answer(info)




