from aiogram.types import Message
import asyncio

from handlers.admin_app.admin_kb_def import create_admin_keyboard
from models import User


async def start_mailing_to_users(message: Message):
    all_users = await User.all()
    semaphore = asyncio.Semaphore(10)

    success_count = 0
    failure_count = 0

    async def send_message(user_id):
        nonlocal success_count, failure_count
        async with semaphore:
            try:
                await message.copy_to(chat_id=user_id)
                success_count += 1
            except Exception as e:
                failure_count += 1
            await asyncio.sleep(0.33)

    tasks = [send_message(user.user_id) for user in all_users]
    await asyncio.gather(*tasks)

    await message.answer(f'<b>📢 Рассылка завершена</b>\n\n'
                         f'Отправилось: <b>{success_count}</b>\n'
                         f'Заблокировали бота: <b>{failure_count}</b>',
                         reply_markup=create_admin_keyboard())