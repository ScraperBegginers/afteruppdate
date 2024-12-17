from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from utils.generate_code import generate_referral_code
from handlers.admin_app.admin_kb_inl import channels_title_name_kb_inl
from config import ADMIN_ID
from handlers.admin_app.admin_kb_def import create_admin_keyboard, create_back_to_admin, manage_channels_kb_def
from handlers.admin_app.admin_middlewaries import BotAdminCheckMiddleware
from handlers.admin_app.mailing_script import start_mailing_to_users
from models import HistoryReferralLinks, ReferralLinks, User
from utils.api_requests import add_channel, def_channel, get_all_channels
from aiogram.exceptions import TelegramAPIError
from tortoise.functions import Count

router = Router()

router.message.outer_middleware(BotAdminCheckMiddleware(ADMIN_ID))
router.callback_query.outer_middleware(BotAdminCheckMiddleware(ADMIN_ID))

@router.message(F.text == 'Назад')
@router.message(Command('admin'))
async def admin_panel(message: types.Message, state: FSMContext):
    await state.clear()

    all_users = await User.all().count()
    await message.answer('<b>Админ панель</b>\n\n'
                         f'Всего пользователей в боте: {all_users}',
                         reply_markup=create_admin_keyboard())

@router.message(F.text == 'Рассылка')
async def enter_message_for_mailing(message: types.Message, state: FSMContext):
    await message.answer('Введите сообщение/фото/gid/файл или что угодно в рассылку\n'
                         '- Разметка поддерживается',
                         reply_markup=create_back_to_admin())
    await state.set_state('mailing_to_1')

@router.message(F.content_type, StateFilter('mailing_to_1'))
async def start_mailing(message: types.Message, state: FSMContext):
    await start_mailing_to_users(message=message)
    await state.clear()
    
@router.message(F.text == 'Управление каналами')
async def manage_channels(message: types.Message, state: FSMContext):
    all_channels = get_all_channels()
    view_channels = [f'{channel["link"]}' for channel in all_channels]
    await message.answer('Все каналы для подписок:\n\n'
                         f'{"\n".join(view_channels)}', disable_web_page_preview=False, reply_markup=manage_channels_kb_def())
                         
@router.message(F.text == 'Добавить канал')
async def enter_new_channel(message: types.Message, state: FSMContext):
    await message.answer('Перешлите сообщение из канала, что бы я мог его добавить', reply_markup=create_back_to_admin())
    await state.set_state('enter_channel_state')
    
@router.message(StateFilter('enter_channel_state'))
async def add_new_channel(message: types.Message, state: FSMContext):
    if not message.forward_from_chat:
        await message.answer("Это не пересланное сообщение из канала. Попробуйте ещё раз.", reply_markup=create_back_to_admin())
        return

    chat_id = message.forward_from_chat.id 
    chat_title = message.forward_from_chat.title

    try:
        admins = await message.bot.get_chat_administrators(chat_id)
        bot_id = await message.bot.me()

        is_bot_admin = any(admin.user.id == bot_id.id for admin in admins)
        if not is_bot_admin:
            await message.answer(f"Бот не является администратором в канале '{chat_title}'. Добавьте бота в администраторы и попробуйте снова.")
            return

        invite_link = await message.bot.export_chat_invite_link(chat_id)
        add_channel(channel_id=chat_id, channel_link=invite_link)

        await message.answer(
            f"✅ Я успешно добавил канал <b>{chat_title}</b>!\n"
            f"ID канала: <code>{chat_id}</code>\n"
            f"Пригласительная ссылка: {invite_link}",
            reply_markup=create_admin_keyboard()
        )
    except TelegramAPIError as e:
        await message.answer(f"Бот не является администратором в канале. Добавьте бота в администраторы и попробуйте снова.",
                              reply_markup=create_admin_keyboard())
    finally:
        await state.clear()
        
@router.message(F.text == 'Удалить канал')
async def enter_chat_for_delete(message: types.Message, state: FSMContext):
    all_channels = get_all_channels()
    
    await message.answer('Выберите канал для удаления',
                         reply_markup=channels_title_name_kb_inl(all_channels=all_channels))
    
@router.callback_query(F.data.startswith('channel_del_'))
async def delete_channel(call: types.CallbackQuery, state: FSMContext):
    channel_for_delete = call.data.removeprefix('channel_del_')
    def_channel(channel_for_delete)
    
    all_channels = get_all_channels()
    
    await call.message.edit_text('Выберите канал для удаления',
                                  reply_markup=channels_title_name_kb_inl(all_channels=all_channels))


@router.message(F.text == 'Создать реферальную ссылку')
async def create_referral_link(message: types.Message, state: FSMContext):
    bot_me = await message.bot.get_me()
    referral_code = generate_referral_code(bot_name=bot_me.username)
    await ReferralLinks(link=referral_code.split('=')[-1]).save()
    
    await message.answer(f'Ваша реферальная ссылка для отслеживания: {referral_code}')
    
@router.message(F.text == 'Статистика по рефералам')
async def check_statisctic(message: types.Message):
    stats = await HistoryReferralLinks.all() \
        .group_by("link") \
        .annotate(count=Count("link")) \
        .values("link", "count")

    if not stats:
        await message.answer("Переходов по реферальным ссылкам пока нет.")
        return


    response = "📊 Статистика по реферальным ссылкам:\n\n"
    for stat in stats:
        response += f"🔗 {stat['link']} - {stat['count']} переходов\n"

    await message.answer(response)