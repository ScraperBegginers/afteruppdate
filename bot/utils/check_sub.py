from utils.api_requests import add_complete_sub, get_all_sub
import asyncio
from time import time
from aiogram.types import ChatMember
from aiogram import Bot

async def check_user_membership(bot: Bot, user_id: int, channel_id: int):
    chat_member: ChatMember = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    if chat_member.status in {'creator', 'administrator', 'member'}:
        return True
    else:
        return False

async def check_sub_to_channel(bot):
    while True:
        try:
            all_sub = get_all_sub().get('subs', [])
            print("Полученные подписки:", all_sub)
                    
            for sub in all_sub:
                if not sub['status_sub'] and float(sub['time_wait']) + 1200 >= time():
                    print(f"Проверка подписки для user_id: {sub['user_id']}, channel_id: {sub['channel_id']}")
                    
                    try:
                        
                        if check_user_membership(bot=bot, user_id=sub['user_id'], channel_id=sub['channel_id']):
                            print(f"Пользователь {sub['user_id']} подписан на канал {sub['channel_id']}")
                            add_complete_sub(user_id=sub['user_id'], channel_id=sub['channel_id'])
                            await asyncio.sleep(1)
                        else:
                            print(f"Пользователь {sub['user_id']} НЕ подписан на канал {sub['channel_id']}")

                    except Exception as e:
                        print(f"Ошибка при проверке подписки: {e}")
                        
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Ошибка в главном цикле: {e}")
            await asyncio.sleep(10)  
