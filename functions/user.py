import config
from bot import botDB, app, bot
from aiogram import html
from functions.members import update_all_db
import datetime
#
#Проверка, является ли пользователь создателем
def user_owner(user_id):
    try:
        role = (botDB.get_all_moderation(user_id)[2])
        if role == 'owner':
            return True
        return False
    except:
        return False

#Проверка, является ли пользователь админом или создателей
def user_admin(user_id):
    try:
        role = (botDB.get_all_moderation(user_id)[2])
        if role == 'admin' or role == 'owner':
            return True
        return False
    except:
        return False

#Генерирует текстовое упоминание пользовател
def get_mention(user):
    name = user.first_name
    id = user.id
    username = user.username
    try:
        if len(username) > 0:
            mention = (f'<a href="t.me/{username}">{html.quote(name)}</a>')
        else:
            mention = (f'<a href="tg://user?id={id}">{html.quote(name)}</a>')
        return mention
    except:
        return name

#получает данные о пользователе для команд
async def get_target(message):
    try:
        if message.reply_to_message:
            try:
                id = message.reply_to_message.from_user.id
                member = await bot.get_chat_member(config.chat_id, id)
                return member
            except:
                return False
        else:
            try:
                target = str(message.text).split()[1]
                if "@" in target:
                    await update_all_db()
                    id = int(str(botDB.get_by_username(target[1:])).split()[1][:-1])
                    member = await bot.get_chat_member(config.chat_id, id)
                    return member
                else:
                    entities = message.entities
                    print(entities)
                    id = int(list(list(entities[1])[4][1])[0][1])
                    member = await bot.get_chat_member(config.chat_id, id)
                    return member
            except:
                return False
    except:
        return False

def time_in_group(user_id):
    date = (botDB.get_all_users(user_id)[2].split()[0].split('-'))
    cur_date = datetime.datetime(day=int(date[2]), month=int(date[1]), year=int(date[0]))
    time_now = datetime.datetime.now()
    time_in_g = (time_now - cur_date).days
    return time_in_g






