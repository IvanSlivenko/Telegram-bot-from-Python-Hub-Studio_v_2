import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN='7012513939:AAGHf4-DSqK9D70av_Vnw-8ADcq5zQ99XiE'

#-------------------------------------------------------- Створюємо бот
bot = Bot(token=TOKEN)
dp = Dispatcher()


#------------------------------------------------------------ Команда /start
@dp.message(CommandStart())
async def start_cmd(message : types.Message):
    await message.answer(f'Привіт.  {message.from_user.first_name}.   Ви активували команду старт')






#---------------------------------------------------- Ехо розташовуємо вкінці
@dp.message()
async def echo(message : types.Message):
    #--------------------------------------------------------
    # text = message.text

    # if  text in ['Привіт' , 'привіт' , 'hi', 'hello']:
    #     await message.answer('І вам привіт')
    # elif text in ['Пока', 'пока', 'до побачення', 'До побачення', 'до побаченя', 'До побаченя']: 
    #     await message.answer('До зустрічі')   
    # else:
    #     await message.answer(message.text)  
    #-------------------------------------------------------
    await message.answer(message.text) 

#------------------------------------------------------ Запускаємо Бот
async def main():
    await dp.start_polling(bot)
asyncio.run(main())
