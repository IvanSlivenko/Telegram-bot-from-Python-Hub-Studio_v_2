import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.strategy import FSMStrategy

#==================================================
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
#==================================================


from handlers.user_privat import user_privat_router
from handlers.user_group import user_group_router
from handlers.user_privat_support import user_privat_router_support
from handlers.admin_privat import admin_router

# from middlewares.db import CounterMiddleware

from common.bot_cmds_list import private
from database.engine import create_db, drop_db, session_marker
from middlewares.db import DataBaseSession


# ALOOWED_UPDATES = ['message', 'edited_message','callback_query'] #----------- Обмеження типів подій

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(
            parse_mode=ParseMode.HTML))
bot.my_admins_list = []

dp = Dispatcher()

# dp.update.outer_middleware(CounterMiddleware())#------------------ реєструємо міделвару в диспетчері
# admin_router.message.middleware(CounterMiddleware())#------------------ реєструємо міделвару в роутері


dp.include_router(user_group_router)
dp.include_router(admin_router)
dp.include_router(user_privat_router_support)
dp.include_router(user_privat_router)



async def on_startup(bot):

    run_param= False
    if run_param:
        await drop_db()
    await create_db()    

async def on_shutdown(bot):
    print('Бот завершив своб  роботу')




#------------------------------------------------------ Запускаємо Бот
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pull=session_marker))

    await create_db()#--------------------------------- Створюємо таблиці в базі данних
    await bot.delete_webhook(drop_pending_updates=True) # ----------------- не реагувати на пропущені повідомлення
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())#------------------ Видалення кнопки та її наповнення
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats()) #------------------ Відображення кнопки та її наповнення
    await dp.start_polling(bot, allowed_updates = dp.resolve_used_update_types())# --------------- Старт бота
asyncio.run(main())
