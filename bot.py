from pyrogram import Client
from aiogram import Bot, Dispatcher
from config import token, userbot_id, userbot_hash
from database import db
#
#bot
bot = Bot(token=token)
dp = Dispatcher()

#userbot
app = Client(name="me_app", api_hash=userbot_hash, api_id=userbot_id, bot_token=token)

#database
botDB = db.botDB('database/users.db')

