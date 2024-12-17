from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_back_to_admin():
    keyboard = [
        [KeyboardButton(text='Назад')]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True)

def create_admin_keyboard():
    keyboard = [
        [
            KeyboardButton(text='Рассылка')
        ],
        [
            KeyboardButton(text='Управление каналами')
        ],
        [
            KeyboardButton(text='Управление ссылками')
        ],
        [
            KeyboardButton(text='Создать реферальную ссылку')
        ],
        [
            KeyboardButton(text='Статистика по рефералам')
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True)

def manage_channels_kb_def():
    keyboard = [
        [
            KeyboardButton(text='Добавить канал'),
            KeyboardButton(text='Удалить канал')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True)
