import traceback

from aiogram import Router
from aiogram.filters import Text, Command, ChatMemberUpdatedFilter, CREATOR, ADMINISTRATOR, MEMBER, RESTRICTED, LEFT, \
    KICKED
from aiogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import bot, botDB, app
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
from aiogram import html
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from handlers.commands.moderation import error_user_not_found
from keyboards.inline import inline_kb
from functions.user import get_mention, time_in_group, get_target
from functions.members import get_messages_count
from functions.time import convert_from_secconds
import random

#Inline KeyBoard
ikb = inline_kb()

router = Router()

#Главная команда
@router.message(Command(commands=["start"]))
async def command_start(message: Message):
    user = message.from_user
    if not message.chat.type == "private":
        return
    if not botDB.user_exists(user.id):
        return await message.answer(f"Привет, {get_mention(user)} ! Чтобы вступить в нашу группу, нажмите на кнопку ниже.", reply_markup=ikb.join_link().as_markup(), parse_mode='HTML', disable_web_page_preview=True)

@router.message(Command(commands=['profile', 'профиль']))
async def profile_command(message: Message):
    user = message.from_user
    get_stats = botDB.get_all_users_stats(user.id)
    stats = get_stats[3]
    if len(message.text.split()) > 1:
        target = (await get_target(message))
        if not target:
            return await message.answer(error_user_not_found)
        user = target.user
    profile_msg = (
        f"Профиль <b>{user.first_name}</b> (<i>{str(get_stats[7])}</i>)\n\n<b>📊Статистика</b>\n<b> ├</b> <i>сообщения:</i> {int(str(stats).split(':')[0]) + int(str(stats).split(':')[1]) + int(str(stats).split(':')[2].split('_')[0]) + int(str(stats).split('_')[1].split(':')[0])}"
        f"\n<b> └</b> <i>репутация:</i> {str(get_stats[2])}"
        f"\n\n<i>С нами уже <b>{time_in_group(user.id)}</b> д.</i>")
    return await message.answer(profile_msg, parse_mode='HTML',disable_notification=True)


#ТОП
#Пока что, самая сложная команда, которую я делал
async def generate_top(type, time, rows=10):
    text1 = {'all':'болтунов', 'text':'болтунов', 'media':'любителей фото', 'photo':'любителей фото', 'video':'любителей видео', 'voice':'любителей голосовых (кол-во)', 'voicecount':'любителей голосовых (кол-во)', 'voicedur':'любителей голосовых (длина)'}.get(type)
    text2 = {1:'за всё время', 2:'за день', 3:'за неделю', 4:'за месяц'}.get(int(time))
    list = {}
    text = ""
    for row in botDB.get_all_users_stats(0):
        usr_id = row[1]
        usr_firstname = botDB.get_all_users(usr_id)[3]
        num = await get_messages_count(type, row[int(time) + 2])
        list[usr_firstname] = num
    list = dict(sorted(list.items(), key=lambda item: item[1], reverse=True))
    position = 1
    for item in list:
        if position <= rows:
            text += f"{position}. <b>{item}</b>: {list[item] if not type == 'voicedur' else convert_from_secconds(list[item])}\n"
            position += 1
    if position < rows:
        for i in range(0, rows - position + 1):
            text += f"{position}. -\n"
            position += 1
    return f"Топ {rows} {text1} {text2}:\n\n{text}"


@router.callback_query(Text(startswith="button_top_"))
async def top_type_callbacks(callback: CallbackQuery):
    buttons = (callback.message.reply_markup.inline_keyboard)
    #await callback.message.answer(f"{buttons}")
    if callback.data.split("_")[2] in "type":
        type = callback.data.split("_")[3]
        list = []
        for button in buttons[-1]:
            list.append(button.text)
        time = (list.index('🔘') + 1)
    elif callback.data.split("_")[2] in "time":
        time = (callback.data.split("_")[3])
        list = []
        if len(buttons) < 3:
            for button in buttons[0]:
                list.append(button.text)
            type = {1:'all', 2:'text', 3:'media', 4:'voice'}.get(list.index('🔘') + 1)
        else:
            for button in buttons[1]:
                if button.text[0] == '✅':
                    list.append(button.text)
            type = {'✅ Фото':'photo', '✅ Видео':'video', '✅ Кол-во':'voicecount', '✅ Длина':'voicedur'}.get(''.join(list))
    else:
        return
    try:
        if type in ['all', 'text']:
            await callback.message.edit_text(f"{await generate_top(type, time)}", reply_markup=ikb.top_buttons(type, time).as_markup(), parse_mode='HTML')
        if type in ['media', 'voice', 'photo', 'video', 'voicecount', 'voicedur']:
            subtype = 2 if type in ['video', 'voicedur'] else 1
            await callback.message.edit_text(f"{await generate_top(type, time)}", reply_markup=ikb.top_buttons(type, time, subtype).as_markup(), parse_mode='HTML')
        await callback.answer("✅")
    except:
        await callback.answer("❌")



@router.message(Command(commands=['top', 'топ']))
async def top_command(message: Message):
    msg = await message.answer("Cекундочку...")
    await msg.edit_text(f"{await generate_top('all', 1, 10)}", parse_mode='HTML', reply_markup=ikb.top_buttons().as_markup())










#special for elbebrioo by XtraF ❤️
@router.message(Command(commands=["huesosit", "хуесосить"]))
async def huesosit_command(message : Message):
    oski = ["Михаил, ебать-копать. \nВот уж чела не сыскать,\nЧто бы так себя любил \nИ жалел, и склонен был \nСам к себе во всем и всяк. \nСлушай, Миша, ты дурак?\nЛучше к сиськам ты тянись.\nТам тебя поднимут ввысь,\nБудут там тебя любить\nИ конец твой теребить,\nПотому что бабы - это\nЦель разврата всего света,\nНу а сам себе и так…\nМиша, Миша ты дурак…\n",
            "Миша - хуевая крыша", "Мишка - потная подмышка", "Миша - полкило кашиша.", "Мишка - в очке крышка.", "Мишка - ёбаный придурок,\nПолуёбок, полудурок,\nКосолапый долбоеб.\nМиша - ёбаный пиздюк.\n", "Миша - тормоз стебанутый,\nТормознутый, психанутый,\nНаркоман, каких сыскать,\nВ жопу трахнутая блядь,\nЕбануто поврежденный,\nНедоделанно рожденный\n",
            "Уронили мишку на пол,\nОторвали мишке лапу,\nВ попу мишке вставлен веник ,\n Мишка должен много денег", "Касумина и Миша шумели на крыше, \nПосле двух выстрелов стало потише!", "Миша, пошёл нахуй !", "Крч, блять, мне лень уже искать дебильные стишки про Мишу, поэтому просто иди нахуй, а стих придумай сам.", "Если ваше имя Миша, то сосите вы потише.",
            "Мишаааа, пора в садик !", "У Миши хуй 2 сантиметра.", "Миша ебаный хуесос.", "Миша, как же я хочу, чтобы тебя выебало Розовое Облако, защекотав твой хуй до смерти, а потом оторвало тебе яйца нахуй, чтобы не выебывался и был добрым.", "Миша, на самом деле я тебя люблю ❤", "Пососи\n\n- Моргенштерн.", "Миша уебан, дай денег на оплату хостинга, пожалуйста.",
            "А вы знали, что Миша недавно ездил в Чечню ?!!! НЕТ ?!!! НУ тогда держите смачные фотки, через пять минут скину."]

    osk = (random.choice(oski))
    await message.answer(f'{osk}', parse_mode='HTML')
