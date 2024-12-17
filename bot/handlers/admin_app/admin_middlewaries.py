from aiogram import BaseMiddleware
from aiogram.types import Message


class BotAdminCheckMiddleware(BaseMiddleware):
    def __init__(self, admin_id: int):
        super().__init__()
        self.admin_id = admin_id

    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id

            if user_id != self.admin_id:
                return None

        return await handler(event, data)