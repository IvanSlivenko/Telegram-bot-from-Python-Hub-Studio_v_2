
from aiogram import F, types,  Router
from aiogram.filters import CommandStart, Command, or_f

from common.contacts_list import contact_shipping
from filters.chat_types import ChatTypeFilter

from kbds import reply
from kbds import reply_custom


user_privat_router = Router()
user_privat_router.message.filter(ChatTypeFilter(['private']))



#------------------------------------------------------------ Команда /start
@user_privat_router.message(CommandStart())
async def start_cmd(message : types.Message):
    await message.answer(f'Привіт.  {message.from_user.first_name}.  Я віртуальний помічник',
                         reply_markup=reply.start_kb_3.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Що вас цікавить'
                            )
                         )
    
@user_privat_router.message(F.text.lower().contains('почат'))
@user_privat_router.message(Command('go'))
async def begin_cmd(message : types.Message):
    await message.answer('Раді вас вітати', reply_markup=reply_custom.start_kb)     


@user_privat_router.message(
        or_f(
            Command('menu'), 
            (F.text.lower().contains('меню')),
            (F.text.lower().contains('функц'))
            )
        )
# @user_privat_router.message(Command('menu'))
async def menu_cmd(message : types.Message):
    await message.answer(f'{message.from_user.first_name}  ви викликали команду меню', reply_markup=reply.del_kbd)
    

@user_privat_router.message(F.text.lower().contains('про нас'))
@user_privat_router.message(Command('about'))
async def about_cmd(message : types.Message):
    await message.answer('Про нас')

@user_privat_router.message((F.text.lower().contains('заплат')) | (F.text.lower().contains('оплат')))
@user_privat_router.message(Command('payment'))
async def payment_cmd(message : types.Message):
    await message.answer('Варіанти оплати')
   

@user_privat_router.message((F.text.lower().contains('привез')) | (F.text.lower().contains('достав'))) # ----------------- contains - шукає збіги у тексті повідомлення
@user_privat_router.message(Command('shipping'))
async def filter_text_custom_contains(message : types.Message):
    await message.answer(f'Вітаємо.\n{message.from_user.first_name} \n з приводу доставки\n ви можете отримати відповіді за телефоном :\n {contact_shipping}')           

@user_privat_router.message(F.text) #------------------------------------------ Текстовий фільтр розташовуємо після всіх  конструкцій
async def filter_text_some(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n Ваш запит :\n "{message.text}"\n ще не зрозумілий для нашої системи ')         


# #---------------------------------------------------- Ехо розташовуємо вкінці
# @user_privat_router.message()
# async def echo(message : types.Message):
#     await message.answer(f' Эхо : {message.text}')



# @user_privat_router.message(F.photo) #------------------------------------------ Фото фільтр
# async def filter_text(message : types.Message):
#     await message.answer(f' Вітаємо. {message.from_user.first_name}  Ви бачете результат роботи магічного фільтра - photo -')



# @user_privat_router.message(F.text.lower() == 'варіанти доставки') #---------- Lower() - переводить усю стрічку  у нижній регістр
# async def filter_text_custom1(message : types.Message):
#     await message.answer(f' Вітаємо. {message.from_user.first_name} з приводу доставки ви можете отримати відповіді за телефоном {contact_shipping}') 


# @user_privat_router.message(Command('shipping'))
# async def shipping_cmd(message : types.Message):
#     await message.answer('Варіанти доставки')
