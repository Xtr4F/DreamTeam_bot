from aiogram import Router, F
from aiogram.filters import Text, Command, ChatMemberUpdatedFilter, CREATOR, ADMINISTRATOR, MEMBER, RESTRICTED, LEFT, KICKED, JOIN_TRANSITION
from aiogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
import traceback
import config
from bot import bot, botDB
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
from aiogram import html
from functions.user import get_mention
from functions.members import add_to_db, set_messages_count, reset_daily_top, reset_weekly_top, reset_monthly_top
import asyncio
import pytz
from datetime import datetime

router = Router()

#Бота нельзя будет добавить в группу, которая не входит в список разрешенных (config/chat_id)
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def check_chat(event: ChatMemberUpdated):
    if not event.chat.id in config.allowed_chats:
        try:
            await bot.send_message(event.chat.id, f"{get_mention(event.from_user)}, я работаю только в разрешенных чатах !", parse_mode='HTML', disable_web_page_preview=True)
            await bot.leave_chat(event.chat.id)
        except:
            pass

@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    join_user = event.new_chat_member.user
    if not botDB.user_exists(join_user.id):
        await bot.send_message(event.chat.id, text=f"<b>👋 Привет, {html.bold(get_mention(join_user))} ! Добро пожаловать в DreamTeam</b>", parse_mode='HTML', disable_web_page_preview=True)
        add_to_db(join_user.id, join_user.first_name, join_user.last_name, join_user.username)
    else:
        await bot.send_message(event.chat.id, text=f"<b>👋 Привет, {html.bold(get_mention(join_user))} ! Рады видеть тебя снова </b>", parse_mode='HTML', disable_web_page_preview=True)

@router.chat_member(ChatMemberUpdatedFilter((CREATOR | ADMINISTRATOR | MEMBER | +RESTRICTED) >> (LEFT)))
async def on_user_leave(event: ChatMemberUpdated):
    await bot.send_message(event.chat.id, text=f"<b>{get_mention(event.from_user)} покинул(-а) группу !</b>", parse_mode='HTML', disable_web_page_preview=True)

@router.chat_member(ChatMemberUpdatedFilter((CREATOR | ADMINISTRATOR | MEMBER | +RESTRICTED) >> (LEFT and KICKED)))
async def on_user_kicked(event: ChatMemberUpdated):
    if not event.from_user.is_bot:
        await bot.send_message(event.chat.id, text=f"<b>Пользователь {get_mention(event.new_chat_member.user)} исключен из группы администратором {get_mention(event.from_user)} !</b>", parse_mode='HTML', disable_web_page_preview=True)



@router.chat_join_request()
async def chat_join_req(message: Message):
    if not botDB.user_exists(message.from_user.id):
        await bot.approve_chat_join_request(message.chat.id, message.from_user.id)
        await bot.send_message(message.from_user.id, text="Ваша заявка на вступление в группу принята !")
    else:
        await bot.send_message(message.from_user.id, text="Ваша заявка на вступление отправлена ! Поскольку Вы были участником группы ранее, заявку должны одобрить администраторы группы.")




@router.message(F.text)
async def handlertext(message: Message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != message.from_user.id:
            if message.text.startswith('+') and len(message.text.split()) < 2:
                botDB.change_reputation(message.reply_to_message.from_user.id, '+')
                await message.answer(f"{get_mention(message.from_user)} увеличил репутацию {get_mention(message.reply_to_message.from_user)}. Теперь его репцтация: {botDB.get_all_users_stats(message.reply_to_message.from_user.id)[2]}", parse_mode='HTML', disable_web_page_preview=True)
            if message.text.startswith('-') and len(message.text.split()) < 2:
                botDB.change_reputation(message.reply_to_message.from_user.id, '-')
                await message.answer(f"{get_mention(message.from_user)} уменьшил репутацию {get_mention(message.reply_to_message.from_user)}. Теперь его репцтация: {botDB.get_all_users_stats(message.reply_to_message.from_user.id)[2]}", parse_mode='HTML', disable_web_page_preview=True)
    if str(message.chat.id) == str(config.chat_id):
        if len(message.text) > 1:
            await set_messages_count(message.from_user.id, "text")

@router.message(F.photo)
async def handlerphoto(message: Message):
    if str(message.chat.id) == str(config.chat_id):
        await set_messages_count(message.from_user.id, "photo")

@router.message(F.video)
async def handlervideo(message: Message):
    if str(message.chat.id) == str(config.chat_id):
        await set_messages_count(message.from_user.id, "video")

@router.message(F.voice)
async def handlervoice(message: Message):
    if str(message.chat.id) == str(config.chat_id):
        duration = int(message.voice.duration)
        await set_messages_count(message.from_user.id, "voice", duration)

@router.message(F.video_note)
async def handlervideonote(message: Message):
    if str(message.chat.id) == str(config.chat_id):
        duration = int(message.video_note.duration)
        await set_messages_count(message.from_user.id, "voice", duration)

async def updates_over_time():
    while True:
        await asyncio.sleep(300)
        date_now = str(datetime.now(tz=config.tz_ru)).split()[0]
        print(date_now)
        try:
            # Обновление ежедневного топа
            if str(botDB.get_all_configs()[1]) != str(date_now):
                day_of_week = datetime.isoweekday(datetime.strptime(str(date_now), '%Y-%m-%d'))
                old_month = (str(botDB.get_all_configs()[1])).split('-')[1]
                botDB.update_date(date_now)
                await reset_daily_top()
                # Обновление еженедельного топа
                if day_of_week == 1:
                    await reset_weekly_top()
                # Обновление ежемесячного топа
                if old_month != (str(botDB.get_all_configs()[1])).split('-')[1]:
                    await reset_monthly_top()
        except:
            try:
                await bot.send_message(config.owner_id, 'Ошибка цикла:\n {traceback.format_exc()}')
            except:
                await bot.send_message(config.owner_id, 'Ошибка цикла')
