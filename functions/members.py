import datetime

from bot import botDB, app, bot
from config import chat_id, owner_id
from functions.time import get_current_time


async def update_all_db():
    users_total = 0
    users_added = 0
    async for member in app.get_chat_members(chat_id):
        try:
            usr_id = member.user.id
            first_name = member.user.first_name
            last_name = member.user.last_name
            user_name = member.user.username
            join_date = member.joined_date
            users_total += 1
            if botDB.user_exists(usr_id):
                botDB.add_first_name(first_name, usr_id)
                botDB.add_last_name(last_name, usr_id)
                botDB.add_user_tag(user_name, usr_id)
            else:
                users_added += 1
                add_to_db(usr_id, first_name, last_name, user_name, join_date)
        except:
            continue
    return f"Проверено: {users_total}\nДобавлено: {users_added}"


def add_to_db(id, first_name, last_name, tag, join_date=0):
    botDB.add_user(id)
    botDB.add_first_name(first_name, id)
    botDB.add_last_name(last_name, id)
    botDB.add_user_tag(tag, id)
    botDB.add_join_date(join_date, id)
    if join_date != 0 and join_date != None:
        return botDB.add_join_date(join_date, id )
    return botDB.add_join_date(get_current_time(), id)

async def get_messages_count(type, text):
    # По кол-ву сообщений разных типов
    if type == 'all':
        return (int(str(text).split(':')[0]) + int(str(text).split(':')[1]) + int(str(text).split(':')[2].split('_')[0]) + int(str(text).split('_')[1].split(':')[0]))
    if type == 'text':
        return (int(str(text).split(':')[0]))
    if type in ['photo', 'media']:
        return (int(str(text).split(':')[1]))
    if type == 'video':
        return (int(str(text).split(':')[2].split('_')[0]))
    if type in ['voicecount', 'voice']:
        return (int(str(text).split('_')[1].split(':')[0]))
    if type == 'voicedur':
        return (int(str(text).split('_')[1].split(':')[1]))

async def set_messages_count(user_id, type, duration=0):
    get_data = botDB.get_all_users_stats(user_id)
    messages = [get_data[3], get_data[4], get_data[5], get_data[6]]
    list = []
    #Код этих сравнений взят из более старой версии проекта, может быть это все можно оптимизировать, но мне так лень, ей богу :)
    if type == 'text':
        for message in messages:
            list.append(f"{int(str(message.split(':')[0])) + 1}:{str(message.split(':', 1)[1])}")
        return botDB.set_messages(user_id, list[0], list[1], list[2], list[3])
    if type == 'photo':
        for message in messages:
            list.append(f"{int(str(message.split(':')[0]))}:{int(str(message.split(':')[1])) + 1}:{str(message.split(':', 2)[2])}")
        return botDB.set_messages(user_id, list[0], list[1], list[2], list[3])
    if type == 'video':
        for message in messages:
            list.append(f"{int(str(message.split(':')[0]))}:{int(str(message.split(':')[1]))}:{int(str(message.split(':')[2])) + 1}_{(str(message.split('_')[1]))}")
        return botDB.set_messages(user_id, list[0], list[1], list[2], list[3])
    if type == 'voice':
        for message in messages:
            list.append(f"{str(message.split('_')[0])}_{int(str(message.split('_')[1]).split(':')[0]) + 1}:{int(str(message.split('_')[1]).split(':')[1]) + int(duration)}")
        return botDB.set_messages(user_id, list[0], list[1], list[2], list[3])

#
async def reset_daily_top():
    for row in botDB.get_all_users_stats(0):
        user_id = row[1]
        botDB.set_messages(user_id, 0, "0:0:0_0:0_0:0", 0, 0)
    await bot.send_message(owner_id, "Ежедневный топ обновлён !")


async def reset_weekly_top():
    for row in botDB.get_all_users_stats(0):
        user_id = row[1]
        botDB.set_messages(user_id, 0, 0, "0:0:0_0:0_0:0", 0)
    await bot.send_message(owner_id, "Еженедельный топ обновлён !")


async def reset_monthly_top():
    for row in botDB.get_all_users_stats(0):
        user_id = row[1]
        botDB.set_messages(user_id, 0, 0, 0, "0:0:0_0:0_0:0")
    await bot.send_message(owner_id, "Ежемесячный топ обновлён !")

