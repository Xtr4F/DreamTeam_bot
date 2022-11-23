#----------------------- ИМПОРТЫ ------------------------------#
from aiogram import Router, html, F
from aiogram.filters import Command, Text, CommandObject
from aiogram.types import Message, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import time
import config
from bot import botDB, bot, dp, app
from functions.user import user_admin, get_mention, get_target, user_owner
from functions.time import convert_to_seconds, convert_to_unix, separate, convert_from_unix, get_time_difference, convert_from_secconds
from functions.syntax import mute_syntax, unmute_syntax, ban_syntax, unban_syntax
from functions.members import update_all_db
from keyboards.inline import inline_kb
#--------------------------------------------------------------#

#Inline KeyBoard
ikb = inline_kb()
router = Router()



error_user_not_admin = "Эта команда только для администраторов бота !"
error_user_not_owner = "Эта команда только для создателя бота !"
error_message_not_reply = "Эта команда должна быть ответом на сообщение !"
error_target_is_bot = "Эта команда не работает на ботов !"
error_user_not_found = "Пользователь не найден, либо никогда не был в группе."
error_command_for_groups = "Эта команда может быть использована только в группе !"


@router.message(Command(commands=["info"]))
async def info_command(message: Message):
    if message.reply_to_message:
        await message.answer(f"Информация о пользователе:\n\n")
        await bot.send_message(message.chat.id, (await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)))


@router.message(Command(commands=["mute", "мут"]))
async def mute_command(message: Message):
    #Проверки
    user = message.from_user
    if not user_admin(user.id):
        return await message.reply(error_user_not_admin)
    if message.chat.type == 'private':
        return await message.answer(error_command_for_groups)
    if not (mute_syntax(message)[0]):
        return await message.reply(mute_syntax(message)[1], parse_mode='HTML')
    target = await get_target(message)
    if not bool(target):
        return await message.reply(error_user_not_found)
    if target.user.is_bot:
        return await message.reply(error_target_is_bot)
    if target.user.id == user.id:
        return await message.reply("Нельзя замутить самого себя :)")
    if target.status in ["administrator", "creator"]:
        return await message.reply("Нельзя замутить администратора")
    if target.status == "restricted" and not (target.can_send_messages and target.can_send_other_messages and target.can_send_polls and target.can_send_media_messages):
            return await message.reply(f"<b><i>Пользователь уже в муте.\nОкончание мута через:</i> \n{convert_from_secconds(get_time_difference(target.until_date))}</b>",parse_mode='HTML')
    #Логика мута
    time = convert_to_seconds(separate(message)[0], separate(message)[1])
    time_unix = convert_to_unix(time[0])
    reason = "".join(list(str(mute_syntax(message)[1])))
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=target.user.id, permissions=ChatPermissions(
                                                                                    can_send_messages=False,
                                                                                    can_send_media_messages=False,
                                                                                    can_send_polls=False,
                                                                                    can_send_other_messages=False,
                                                                                    can_add_web_page_previews=False,
                                                                                    can_invite_users=False),
                                                                                    until_date=time_unix)
    return await message.answer(f'<b>{get_mention(user)} замутил пользователя {get_mention(target.user)} на {time[2]} {time[1]} {reason}</b>', parse_mode='HTML', disable_web_page_preview=True)


@router.message(Command(commands=["unmute", "анмут", "размут"]))
async def unmute_command(message: Message):
    #Проверки
    if not user_admin(message.from_user.id):
        return await message.reply(error_user_not_admin)
    if message.chat.type == 'private':
        return await message.answer(error_command_for_groups)
    if not (unmute_syntax(message)[0]):
        return await message.reply(unmute_syntax(message)[1], parse_mode='HTML')
    target = await get_target(message)
    if not bool(target):
        return await message.reply(error_user_not_found)
    if not target.status == "restricted" and not (target.can_send_messages and target.can_send_other_messages and target.can_send_polls and target.can_send_media_messages):
        return await message.reply("У пользователя нет мута.")
    #Логика размута
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=target.user.id, permissions=ChatPermissions(
                                                               can_send_messages=True,
                                                               can_send_media_messages=True,
                                                               can_send_polls=True,
                                                               can_send_other_messages=True,
                                                               can_add_web_page_previews=True,
                                                               can_change_info=True,
                                                               can_invite_users=True,
                                                               can_pin_messages=True))
    return await message.answer(f'{get_mention(message.from_user)} снял мут с {get_mention(target.user)} !', parse_mode='HTML', disable_web_page_preview=True)


@router.message(Command(commands=["ban", "бан"]))
async def ban_command(message: Message):
    #Проверки
    if not user_admin(message.from_user.id):
        return await message.reply(error_user_not_admin)
    if message.chat.type == 'private':
        return await message.answer(error_command_for_groups)
    if not (ban_syntax(message)[0]):
        return await message.reply(ban_syntax(message)[1], parse_mode='HTML')
    target = await get_target(message)
    if not bool(target):
        return await message.reply(error_user_not_found)
    if target.user.id == message.from_user.id:
        return await message.reply("Нельзя забанить самого себя :)")
    if target.status in ["administrator", "creator"]:
        return await message.reply("Нельзя забанить администратора")
    if target.status in "kicked":
        return message.reply("Пользователь уже забанен")
    #Логика бана
    reason = "".join(ban_syntax(message)[1])
    await bot.ban_chat_member(message.chat.id, target.user.id)
    await message.answer(f"{get_mention(message.from_user)} забанил {get_mention(target.user)} ! {reason}", parse_mode='HTML', disable_web_page_preview=True)
    try:
        await bot.send_message(target.user.id, f"Вы были забанены в группе ! {reason}", parse_mode='HTML')
    except:
        pass

@router.message(Command(commands=["unban", "разбан"]))
async def unban_command(message: Message):
    # Проверки
    if not user_admin(message.from_user.id):
        return await message.reply(error_user_not_admin)
    if message.chat.type == 'private':
        return await message.answer(error_command_for_groups)
    if not (unban_syntax(message)[0]):
        return await message.reply(unban_syntax(message)[1], parse_mode='HTML')
    target = await get_target(message)
    if not bool(target):
        return await message.reply(error_user_not_found)
    if not target.status in "kicked":
        return message.reply("У пользователя нет бана.")
    #Логика разбана
    await bot.unban_chat_member(message.chat.id, target.user.id)
    await message.answer(f"{get_mention(message.from_user)} cнял бан с {get_mention(target.user)} !", parse_mode='HTML', disable_web_page_preview=True)
    try:
        await bot.send_message(target.user.id, f"Вы были разбанены в группе ! Вы можете вступить в нее снова, нажав на кнопку ниже.", parse_mode='HTML' ,reply_markup=ikb.join_link().as_markup())
    except:
        pass


@router.message(Command(commands=["reload_db"]))
async def reload_db_command(message: Message):
    if not ((user_owner(message.from_user.id)) or (str(message.from_user.id) in str(config.owner_id))):
        return await message.answer(error_user_not_owner)
    await message.answer("Запущено")
    start_time = time.time()
    reload = await update_all_db()
    end_time = (f"{(time.time() - start_time)} сек.")
    return await message.answer(f"Сбор данных окончен.\n{reload}\n\nКоманда выполнена за:\n{end_time}",parse_mode='HTML')

@router.message(Command(commands=["add_admin"]))
async def add_admin_command(message: Message):
    if not ((user_owner(message.from_user.id)) or (str(message.from_user.id) in str(config.owner_id))):
        return await message.answer(error_user_not_owner)
    if len(message.text.split()) < 2:
        return await message.answer("Вы не указали пользователя !")
    target = (await get_target(message))
    if not target:
        return await message.answer(error_user_not_found)
    if user_admin(target.user.id):
        return await message.answer("Пользователь уже админ !")
    botDB.change_role(target.user.id, "admin")
    return await bot.send_message(config.chat_id, "{get_mention(target.user)} добавлен в админы бота !", parse_mode='HTML', disable_web_page_preview=True)


#hui

@router.message(Command(commands=["del_admin"]))
async def del_admin_command(message: Message):
    if not ((user_owner(message.from_user.id)) or (str(message.from_user.id) in str(config.owner_id))):
        return await message.answer(error_user_not_owner)
    if len(message.text.split()) < 2:
        return await message.answer("Вы не указали пользователя !")
    target = (await get_target(message))
    if not target:
        return await message.answer(error_user_not_found)
    if not user_admin(target.user.id):
        return await message.answer("Пользователь не админ !")
    botDB.change_role(target.user.id, "user")
    return await bot.send_message(config.chat_id, f"{get_mention(target.user)} удален из списка администраторов бота !", parse_mode='HTML', disable_web_page_preview=True)

@router.message(Command(commands=['pin', 'закрепить']))
async def pin_command(message: Message):
    if not message.reply_to_message:
        return await message.reply(f"{error_message_not_reply}")
    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    await message.delete()

@router.message(Command(commands=['unpin', 'открепить']))
async def pin_command(message: Message):
    if not user_admin(message.from_user.id):
        return await message.reply(error_user_not_admin)
    if not message.reply_to_message:
        return await message.reply(f"{error_message_not_reply}")
    await bot.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
    await message.delete()

@router.message(Command(commands=['tell', 'say']))
async def tell_command(message: Message, command: CommandObject):
    if not user_admin(message.from_user.id):
        return await message.reply(error_user_not_admin)
    await message.delete()
    text = command.args
    if text.split()[-1] == "NOHTML":
        return await bot.send_message(config.chat_id, text[:6])
    await bot.send_message(config.chat_id, text, parse_mode='HTML')































































































  