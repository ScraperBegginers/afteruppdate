from aiogram.types import ChatMember
from utils.api_requests import add_complete_sub, get_all_sub
import asyncio
from time import time

async def check_sub_to_channel(bot):
    
    while True:
        all_sub = get_all_sub()['subs']
        print(all_sub)
                
        for sub in all_sub:
            if sub['status_sub'] is False:
                if float(sub['time_wait'] + 600) <= time():
                
                    chat_member = await bot.get_chat_member(chat_id=sub['channel_id'], user_id=sub['user_id'])
                    print(chat_member.status)
                    if chat_member.status:
                        add_complete_sub(user_id=sub['user_id'], channel_id=sub['channel_id'])
                        await asyncio.sleep(1)
                    
            
        await asyncio.sleep(5)