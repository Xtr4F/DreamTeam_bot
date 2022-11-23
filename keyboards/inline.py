from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class inline_kb:
    def join_link(self):
        buttons = InlineKeyboardBuilder()
        buttons.add(InlineKeyboardButton(text="Вступить в группу", url="https://t.me/+HSZOJoIlY2c1MDUy"),
                    InlineKeyboardButton(text="Запасная ссылка", url="https://t.me/+mZmYUdMohetjZTYy"))
        return buttons

    def top_buttons(self, selected_type='all', selected_time=1, subselected=1):
        buttons = InlineKeyboardBuilder()
        #Добавляем кнопки смены типа
        buttons.row(InlineKeyboardButton(text=("🔘" if selected_type == 'all' else "⚪️"), callback_data="button_top_type_all"),
                    InlineKeyboardButton(text=("🔘" if selected_type == 'text' else "⚪️"), callback_data="button_top_type_text"),
                    InlineKeyboardButton(text=("🔘" if selected_type in ['media', 'photo', 'video'] else "⚪️"), callback_data="button_top_type_media"),
                    InlineKeyboardButton(text=("🔘" if selected_type in ['voice', 'voicecount', 'voicedur'] else "⚪️"), callback_data="button_top_type_voice"))
        #Добавляем дополнительный подуровень кнопок типа
        if selected_type in ['media', 'photo', 'video']:
            buttons.row(InlineKeyboardButton(text=("✅ Фото" if subselected == 1 else "Фото"), callback_data="button_top_type_photo"),
                        InlineKeyboardButton(text=("✅ Видео" if subselected == 2 else "Видео"), callback_data="button_top_type_video"))
        if selected_type in ['voice', 'voicecount', 'voicedur']:
            buttons.row(InlineKeyboardButton(text=("✅ Кол-во" if subselected == 1 else "Кол-во"), callback_data="button_top_type_voicecount"),
                        InlineKeyboardButton(text=("✅ Длина" if subselected == 2 else "Длина"), callback_data="button_top_type_voicedur"))
        #Добавляем кнопки смены времени
        buttons.row(InlineKeyboardButton(text=("🔘" if int(selected_time) == 1 else "⚪️"), callback_data="button_top_time_1"), #all
                    InlineKeyboardButton(text=("🔘" if int(selected_time) == 2 else "⚪️"), callback_data="button_top_time_2"), #day
                    InlineKeyboardButton(text=("🔘" if int(selected_time) == 3 else "⚪️"), callback_data="button_top_time_3"), #week
                    InlineKeyboardButton(text=("🔘" if int(selected_time) == 4 else "⚪️"), callback_data="button_top_time_4")) #month
        #Возвращаем клавитауру
        return buttons
