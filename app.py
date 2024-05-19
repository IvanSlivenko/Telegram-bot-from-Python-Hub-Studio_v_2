import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

#==================================================
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
#==================================================


from handlers.user_privat import user_privat_router
from handlers.user_group import user_group_router
from handlers.user_privat_support import user_privat_router_support
from common.bot_cmds_list import private


ALOOWED_UPDATES = ['message', 'edited_message'] #----------- Обмеження типів подій

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(user_group_router)
dp.include_router(user_privat_router_support)
dp.include_router(user_privat_router)







#------------------------------------------------------ Запускаємо Бот
async def main():
    await bot.delete_webhook(drop_pending_updates=True) # ----------------- не реагувати на пропущені повідомлення
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())#------------------ Видалення кнопки та її наповнення
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats()) #------------------ Відображення кнопки та її наповнення
    await dp.start_polling(bot, allowed_updates = ALOOWED_UPDATES)# --------------- Старт бота
asyncio.run(main())
