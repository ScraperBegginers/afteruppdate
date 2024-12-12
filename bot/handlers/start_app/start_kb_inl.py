from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from bot.utils.reader_config import get_urls


def create_kb_start():
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Играть', web_app=WebAppInfo(url='https://google.com'))
        ],
        [
            InlineKeyboardButton(text='Отзывы', url=get_urls('reviews')),
            InlineKeyboardButton(text='Менеджер', url=get_urls('manager'))
        ],
        [
            InlineKeyboardButton(text='Новости', url=get_urls('news')),
            InlineKeyboardButton(text='Обучение', url=get_urls('tutorials'))
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)