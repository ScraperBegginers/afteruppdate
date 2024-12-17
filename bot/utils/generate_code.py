import random
import string

def generate_referral_code(bot_name):
    characters = string.ascii_uppercase + string.digits 
    referral_code = ''.join(random.choices(characters, k=10))
    return f'https://t.me/{bot_name}?start={referral_code}'