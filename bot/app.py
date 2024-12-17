import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils.check_sub import check_sub_to_channel
from database.database_db import init_db
from handlers.start_app import start
from handlers.admin_app import admin
from utils.middlewaries.check_sub import SubscriptionMiddleware
from config import BOT_TOKEN

dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.message.middleware(SubscriptionMiddleware(bot))
    dp.callback_query.middleware(SubscriptionMiddleware(bot))

    dp.include_router(start.router)

    dp.include_router(admin.router)
    
    loop = asyncio.get_event_loop()
    loop.create_task(check_sub_to_channel(bot=bot))
    
    await init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

