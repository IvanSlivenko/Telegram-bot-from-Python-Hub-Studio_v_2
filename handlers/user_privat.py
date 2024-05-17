
from aiogram import types,  Router
from aiogram.filters import CommandStart, Command
user_privat_router = Router()




#------------------------------------------------------------ Команда /start
@user_privat_router.message(CommandStart())
async def start_cmd(message : types.Message):
    await message.answer(f'Привіт.  {message.from_user.first_name}.  Я віртуальний помічник')

#---------------------------------------------------- Ехо розташовуємо вкінці
@user_privat_router.message(Command('menu'))
async def echo(message : types.Message):
    await message.answer(f'{message.from_user.first_name}  ви викликали команду меню')


# #---------------------------------------------------- Ехо розташовуємо вкінці
# @user_privat_router.message()
# async def echo(message : types.Message):
#     await message.answer(f' Эхо : {message.text}')
    
