from aiogram.types import ChatMemberStatus
from bot.utils.api_requests import get_all_sub
import asyncio

async def check_sub_to_channel(bot):
    
    while True:
        all_sub = get_all_sub()['subs']
        
        for sub in all_sub:
             chat_member = await bot.get_chat_member(chat_id=sub['channel_id'], user_id=sub['user_id'])
             
             if chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                 pass 
             
             await asyncio.sleep(1)
            
        await asyncio.sleep(5)