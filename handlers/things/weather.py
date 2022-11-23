import requests, asyncio
from bot import bot
from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.types import Message, ChatPermissions, User, Chat
from config import WEATHER_TOKEN
from datetime import datetime
from pytz import timezone
from functions.time import convert_from_unix
from dateutil.tz import *

import traceback

router = Router()

#
def ToD(time):
    hours = int(time.split(':')[0])
    return ("🌌 Ночь" if hours <= 6 else("🌄 Утро" if hours < 12 else("🏞 День" if hours < 18 else "🌆 Вечер")))


@router.message(Command(commands=['weather', 'погода']))
async def weather_command(message: Message):
    if len(message.text.split()) < 2:
        return await message.answer(f"<b>Вы не указали город/посёлок.</b>", parse_mode='HTML')
    try:
        city = " ".join(message.text.split()[1:len(message.text.split())])
        try:
            data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}&units=metric").json()
        except:
            return await message.answer("Лимит запросов в день исчерпан. Каким, бть образом ?! :(")
        tz = data["timezone"]
        cur_time = str(datetime.now(tzoffset("t", tz))).split('.')[0].split()[1]
        cur_date = str(datetime.now(tzoffset("t", tz))).split('.')[0].split()[0]
        times_of_day = ToD(str(cur_time))
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        weather_type = data["weather"][0]["main"]
        wd = {"Clouds": "☁ Облачно", "Rain": "🌧 Дождь", "Drizzle": "🌧 Слабый дождь", "Thunderstorm": "⛈ Гроза", "Snow": "🌨 Снег", "Mist": "🌫 Туман",
              "Clear": "🌙 Ясно" if int(str(cur_time).split(':')[0]) <= 6 else "☀ Ясно"}.get(weather_type)
        sunrise_time = str(datetime.fromtimestamp(data["sys"]["sunrise"]).astimezone(tzoffset('t', tz))).split('.')[0].split()[1].split('+')[0].split('-')[0]
        sunset_time = str(datetime.fromtimestamp(data["sys"]["sunset"]).astimezone(tzoffset('t', tz))).split('.')[0].split()[1].split('+')[0].split('-')[0]
        day_length = str(datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.fromtimestamp(data["sys"]["sunrise"]))
        await message.reply(
            f"<b>Погода в {city}:</b>\n\n<b>{wd}</b> ({times_of_day} <i>{cur_time[0:-3]}</i>)\n\n"
            f"<b>🌡 Температура</b> {temp} C°\n<b>💦 Влажность</b> {humidity}%\n"
            f"<b>💨 Ветер</b> {wind_speed} м/с\n<b>⏱ Давление</b> {pressure} гПа\n\n"
            f"<b>🌄 Восход: </b><i>{sunrise_time}</i>\n<b>🌇 Закат: </b><i>{sunset_time}</i>\n\n<b>🏙 Продолж. дня: </b><i>{day_length}</i>"
            f"", parse_mode='HTML', disable_notification=True)
    except:
        await message.answer(f"<b>Вы неправильно указали город/посёлок. Пожалуйста, проверьте правильность и попробуйте снова.</b>", parse_mode='HTML')