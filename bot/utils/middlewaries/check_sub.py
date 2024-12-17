from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Callable, Dict, Any, Awaitable

from utils.get_photo import read_photo
from utils.reader_config import get_channel_id


async def check_subscribe_to_channel(bot, user_id: int):
    get_channel = get_channel_id()
    user_channel_status = await bot.get_chat_member(chat_id=get_channel, user_id=user_id)
    if user_channel_status.status == 'left':
        return False
    else:
        return True


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[CallbackQuery], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        check = await check_subscribe_to_channel(bot=self.bot, user_id=user_id)

        if not check:
            get_link = await event.bot.get_chat(get_channel_id())
            inline_keyboard = [
                [InlineKeyboardButton(text='Перейти в канал', url=get_link.invite_link)],
                [InlineKeyboardButton(text='Продолжить', callback_data='continue')]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            try:
                await event.answer_photo(photo=await read_photo('start_login'),
                                                 caption="<b>Увы, Вы не подписаны на наш Telegram-канал.</b>\n\n"
                                                         "Подпишитесь и нажмите <b>'Продолжить'.</b>",
                                                 reply_markup=markup)
            except AttributeError:
                await event.answer('Вы не подписаны на канал', show_alert=True)
            return

        return await handler(event, data)
