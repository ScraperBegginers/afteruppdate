from aiogram.types import Message
from aiogram.utils.payload import decode_payload

from utils.api_requests import add_referral
from models import HistoryReferralLinks, ReferralLinks, User


async def checking_referral(message: Message):
    inviter_referral_id_encode = message.text.split(' ')[-1]


    if inviter_referral_id_encode != '/start':
        check_referral_link = await ReferralLinks.get_or_none(link=inviter_referral_id_encode)
        if check_referral_link:
            get_no_double = await HistoryReferralLinks.get_or_none(link=inviter_referral_id_encode, user_id=message.from_user.id)
            if get_no_double:
                return
            
            await HistoryReferralLinks(link=inviter_referral_id_encode, user_id=message.from_user.id).save()
        else:
            inviter_referral_id = inviter_referral_id_encode
            referral = message.from_user.id

            add_referral(referral_id=inviter_referral_id, user_id=referral)