



command_error = {
    "not_time_type" : "<i><b>⚠️ Ошибка.</b> Вы не указали тип времени <b>(m, h или d).</b></i>",
    "wrong_time" : "<i><b>⚠️ Ошибка.</b> Вы неправильно указали время мута.</i>",
    "not_time" : "<i><b>⚠️ Ошибка.</b> Вы не указали время мута.</i>",
    "wrong_user" : "<i><b>⚠️Ошибка.</b> Вы неправильно указали пользователя.</i>",
    "not_enough_arguments" : "<i><b>⚠️ Ошибка.</b> Команде не хватает аргументов.</i>"
}



#
def mute_syntax(message):
    mute_right = {
        1: "\n\n<b>📌 Правильно:</b>\n<CODE>/mute [ВРЕМЯ][m/h/d]</CODE>\n<CODE>/mute 10h</CODE>",
        2: "\n\n<b>📌 Правильно:</b>\n<CODE>/mute [ТЭГ] [ВРЕМЯ][m/h/d]</CODE>\n<CODE>/mute @elbebrioo 10h</CODE>"}
    text = str(message.text)
    length = len(text.split())
    reason = ""
    if message.reply_to_message:
        if length < 2:
            return [False, f'{command_error.get("not_enough_arguments")} <b>(Время)</b> {mute_right.get(0)}']
        if (text.split()[1][:1].isdigit()) and (text.split()[1][-1] in ['m', 'h', 'd']):
            if length > 2:
                reason = f"Причина: {''.join(text.split()[2:length])}"
            return [True, reason]
        return [False, f'{command_error.get("wrong_time")}{mute_right.get(0)}']
    else:
        if length < 3:
            return [False, f'{command_error.get("not_enough_arguments")} <b>(Пользователь, Время)</b> {mute_right.get(2)}'] if length < 2 else [False, f'{command_error.get("not_enough_arguments")} <b>(Время)</b> {mute_right.get(2)}']
        if "@" in text.split()[1] or ("text_mention" in str(message.entities) and text.split()[1] in str(message.entities)):
            if (text.split()[2][:1].isdigit()) and (text.split()[2][-1] in ['m', 'h', 'd']):
                if length > 3:
                    reason = f"Причина: {''.join(text.split()[3:length])}"
                return [True, reason]
            return [False, f'{command_error.get("wrong_time")}{mute_right.get(2)}']
        return [False, f'{command_error.get("wrong_user")}{mute_right.get(2)}']


def unmute_syntax(message):
    unmute_right = "\n\n<b>📌 Правильно:</b>\n<CODE>/unmute [ТЭГ]</CODE>\n<CODE>/unmute @elbebrioo</CODE>"
    text = message.text
    if message.reply_to_message:
        return [True]
    if len(text.split()) < 2:
        return [False, f'{command_error.get("not_enough_arguments")} <b>(Пользователь)</b>{unmute_right}']
    if "@" in text.split()[1] or ("text_mention" in str(message.entities) and text.split()[1] in str(message.entities)):
        return [True]
    return [False, f'{command_error.get("wrong_user")}{unmute_right}']

def ban_syntax(message):
    ban_right = "\n\n<b>📌 Правильно:</b>\n<CODE>/ban [ТЭГ]</CODE>\n<CODE>/ban @elbebrioo бебрик</CODE>"
    text = message.text
    length = len(text.split())
    reason = ""
    if message.reply_to_message:
        if length > 1:
            reason = f"Причина: {''.join(text.split()[1:length])}"
        return [True, reason]
    if length < 2:
        return [False, f'{command_error.get("not_enough_arguments")} <b>(Пользователь)</b>{ban_right}']
    if "@" in text.split()[1] or ("text_mention" in str(message.entities) and text.split()[1] in str(message.entities)):
        if length > 2:
            reason = f"Причина: {''.join(text.split()[2:length])}"
        return [True, reason]
    return [False, f'{command_error.get("wrong_user")}{ban_right}']

def unban_syntax(message):
    unban_right = "\n\n<b>📌 Правильно:</b>\n<CODE>/unban [ТЭГ]</CODE>\n<CODE>/unmute @elbebrioo</CODE>"
    text = message.text
    if message.reply_to_message:
        return [True]
    if len(text.split()) < 2:
        return [False, f'{command_error.get("not_enough_arguments")} <b>(Пользователь)</b>{unban_right}']
    if "@" in text.split()[1] or (
            "text_mention" in str(message.entities) and text.split()[1] in str(message.entities)):
        return [True]
    return [False, f'{command_error.get("wrong_user")}{unban_right}']
















