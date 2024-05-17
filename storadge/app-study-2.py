import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())



#-------------------------------------------------------- Створюємо бот
# from config import TOKEN
# bot = Bot(token=TOKEN)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


#------------------------------------------------------------ Команда /start
@dp.message(CommandStart())
async def start_cmd(message : types.Message):
    await message.answer(f'Привіт.  {message.from_user.first_name}.   Ви активували команду старт')






#---------------------------------------------------- Ехо розташовуємо вкінці
@dp.message()
async def echo(message : types.Message, bot: Bot):
    #--------------------------------------------------------
    # text = message.text

    # if  text in ['Привіт' , 'привіт' , 'hi', 'hello']:
    #     await message.answer('І вам привіт')
    # elif text in ['Пока', 'пока', 'до побачення', 'До побачення', 'до побаченя', 'До побаченя']: 
    #     await message.answer('До зустрічі')   
    # else:
    #     await message.answer(message.text)  
    #-------------------------------------------------------
    # await message.reply(message.text)

    await message.answer(f' Эхо : {message.text}')
    

#------------------------------------------------------ Запускаємо Бот
async def main():
    await bot.delete_webhook(drop_pending_updates=True) # ----------------- не реагувати на пропущені повідомлення
    await dp.start_polling(bot)
asyncio.run(main())
