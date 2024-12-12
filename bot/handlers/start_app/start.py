from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.handlers.start_app.start_kb_inl import create_kb_start
from bot.handlers.start_app.start_text import start_text
from bot.models import User
from bot.utils.get_photo import read_photo

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext):
    await state.clear()

    user, created = await User.get_or_create(user_id=message.from_user.id, defaults={
        'username': message.from_user.username
    })

    if not created:
        if user.username != message.from_user.username:
            user.username = message.from_user.username
            await user.save()

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