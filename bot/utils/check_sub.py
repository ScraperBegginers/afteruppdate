

from bot.utils.api_requests import get_all_sub


async def check_sub_to_channel(bot):
    
    while True:
        all_sub = get_all_sub()['subs']
        
        for sub in all_sub:
            pass