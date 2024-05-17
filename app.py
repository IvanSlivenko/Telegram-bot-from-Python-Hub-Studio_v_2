import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

#==================================================
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
#==================================================


from handlers.user_privat import user_privat_router




ALOOWED_UPDATES = ['message', 'edited_message'] #----------- Обмеження типів подій

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(user_privat_router)



#------------------------------------------------------ Запускаємо Бот
async def main():
    await bot.delete_webhook(drop_pending_updates=True) # ----------------- не реагувати на пропущені повідомлення
    await dp.start_polling(bot, allowed_updates = ALOOWED_UPDATES)
asyncio.run(main())
