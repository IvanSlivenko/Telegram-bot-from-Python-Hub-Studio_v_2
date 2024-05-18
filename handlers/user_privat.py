
from aiogram import F, types,  Router
from aiogram.filters import CommandStart, Command
user_privat_router = Router()

from common.contacts_list import contact_shipping


#------------------------------------------------------------ Команда /start
@user_privat_router.message(CommandStart())
async def start_cmd(message : types.Message):
    await message.answer(f'Привіт.  {message.from_user.first_name}.  Я віртуальний помічник')


@user_privat_router.message(Command('menu'))
async def menu_cmd(message : types.Message):
    await message.answer(f'{message.from_user.first_name}  ви викликали команду меню')


@user_privat_router.message(Command('about'))
async def about_cmd(message : types.Message):
    await message.answer('Про нас')


@user_privat_router.message(Command('payment'))
async def payment_cmd(message : types.Message):
    await message.answer('Варіанти оплати')


@user_privat_router.message(Command('shipping'))
async def shipping_cmd(message : types.Message):
    await message.answer('Варіанти доставки')

@user_privat_router.message(Command('catalog'))
async def catalog_cmd(message : types.Message):
    await message.answer('Тут буде каталог')      

@user_privat_router.message(F.photo) #------------------------------------------ Фото фільтр
async def filter_text(message : types.Message):
    await message.answer(f' Вітаємо. {message.from_user.first_name}  Ви бачете результат роботи магічного фільтра - photo -')

@user_privat_router.message(F.text == 'варіанти доставки')
async def filter_text_custom1(message : types.Message):
    await message.answer(f' Вітаємо. {message.from_user.first_name} з приводу доставки ви можете отримати відповіді за телефоном {contact_shipping}')      

@user_privat_router.message(F.text) #------------------------------------------ Текстовий фільтр розташовуємо після всіх командних конструкцій
async def filter_photo(message : types.Message):
    await message.answer(f' Вітаємо. {message.from_user.first_name}  Ви бачете результат роботи магічного фільтра - text - ')         


# #---------------------------------------------------- Ехо розташовуємо вкінці
# @user_privat_router.message()
# async def echo(message : types.Message):
#     await message.answer(f' Эхо : {message.text}')
    
