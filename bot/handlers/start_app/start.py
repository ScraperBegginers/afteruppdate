from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from handlers.start_app.referral_script import checking_referral
from handlers.start_app.start_kb_inl import create_kb_start
from handlers.start_app.start_text import start_text
from models import User
from utils.get_photo import read_photo
from utils.api_requests import create_user

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext):
    await state.clear()

    user, created = await User.get_or_create(user_id=message.from_user.id, defaults={
        'username': message.from_user.username
    })
    
    if created:
        create_user(user_id=message.from_user.id, first_name=message.from_user.first_name, username=message.from_user.username)

    await checking_referral(message=message)
    await message.answer_photo(
        photo=await read_photo('start_menu'),
        caption=start_text(),
        reply_markup=create_kb_start()
    )

@router.callback_query(F.data == 'continue')
async def start_message_editing(call: types.CallbackQuery):
    photo = await read_photo('start_menu')
    await call.message.edit_media(
        media=types.InputMediaPhoto(
            media=photo,
            caption=start_text()
        ),
        reply_markup=create_kb_start()
    )