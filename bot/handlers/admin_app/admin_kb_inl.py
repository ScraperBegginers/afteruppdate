from aiogram.utils.keyboard import InlineKeyboardBuilder

def channels_title_name_kb_inl(all_channels: list):
    keyboard = InlineKeyboardBuilder()
    
    for channel in all_channels:
        keyboard.button(
            text=channel['link'],
            callback_data=f'channel_del_' + str(channel['channel_id'])
        )
    
    keyboard.adjust(1, 1)
    return keyboard.as_markup()