import datetime
from datetime import timedelta, timezone
import config

#Конвертирует время в секунды
def convert_to_seconds(time, preffix):
    if preffix == "m":
        return [(int(time) * 60), str('мин.'), int(time)]
    if preffix == "h":
        return [(int(time) * 3600), str('ч.'), int(time)]
    if preffix == "d":
        return [(int(time) * 86400), str('д.'), int(time)]

def convert_from_secconds(time):
    sec = time
    delta = str(timedelta(seconds=sec))
    result = ""
    if sec >= 86400:
        hms = delta.split()[2]
        converted = [f"{int(delta.split()[0])}д.", f"{int(hms.split(':')[0])}ч.", f"{int(hms.split(':')[1])}м.", f"{int(hms.split(':')[2])}с."]
    elif sec >= 3600:
        converted = [f"{int(delta.split(':')[0])}ч.", f"{int(delta.split(':')[1])}м.", f"{int(delta.split(':')[2])}с."]
    elif sec >= 60:
        converted = [f"{int(delta.split(':')[1])}м.", f"{int(delta.split(':')[2])}с."]
    else:
        converted = [f"{int(delta.split(':')[2])}с."]
    for num in converted:
        result += f"{num} "
    return result

#разности времени
def get_time_difference(date):
    cur_utc = datetime.datetime.now(timezone.utc)
    delta = date - cur_utc
    return int(delta.total_seconds())

#Конвертирует время в формат UNIX
def convert_to_unix(time):
    time_now = datetime.datetime.now()
    end_time = time_now + datetime.timedelta(seconds=int(time))
    unix = str(end_time.timestamp())
    return unix

#Конвертирует время из UNIX
def convert_from_unix(time):
    date = datetime.datetime.fromtimestamp(float(time)).strftime('%Y-%m-%d %H:%M:%S')
    return date
#
#Получить текущее время (МСК)
def get_current_time():
    current_date = datetime.datetime.now(config.tz_ru)
    return(current_date.strftime("%Y-%m-%d %H:%M:%S"))

#Разделяет время на дату и тип (Например. Input: 10d; Output: ('10', 'd')
def separate(message):
    text = message.text
    if message.reply_to_message:
        if (text.split()[1][-1] in ['m', 'h', 'd']) and (text.split()[1][:1].isdigit()):
            return text.split()[1][0:-1], text.split()[1][-1]
        elif (text.split()[2] in ['m', 'h', 'd']) and (text.split()[1].isdigit()):
            return text.split()[1], text.split()[2]
    else:
        if (text.split()[2][-1] in ['m', 'h', 'd']) and (text.split()[2][:1].isdigit()):
            return text.split()[2][0:-1], text.split()[2][-1]
        elif (text.split()[3] in ['m', 'h', 'd']) and (text.split()[2].isdigit()):
            return text.split()[2], text.split()[3]
