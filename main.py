import asyncio
from bot import bot, dp, app
from handlers.commands import moderation, commands
from handlers.things import weather
from handlers.chat import member

#

async def start_bot():
    print("Запуск бота")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), polling_timeout=10)

async def start_userbot():
    print("Запуск юзербота")
    await app.start()

async def main():
    t1 = asyncio.create_task(start_userbot())
    t2 = asyncio.create_task(start_bot())
    t3 = asyncio.create_task(member.updates_over_time())
    await t1
    await t2
    await t3



if __name__ == '__main__':
    dp.include_router(commands.router)
    dp.include_router(moderation.router)
    dp.include_router(weather.router)
    dp.include_router(member.router)
    asyncio.run(main())