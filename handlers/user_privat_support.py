
from aiogram import F, types,  Router
from aiogram.filters import CommandStart, Command, or_f

from common.contacts_list import contact_shipping, contact_consult, contact_assembling, contact_cashier
from filters.chat_types import ChatTypeFilter

from kbds import reply
from kbds import reply_custom

user_privat_router_support = Router()
user_privat_router_support.message.filter(ChatTypeFilter(['private']))

@user_privat_router_support.message(F.text.lower().contains('каталог'))
@user_privat_router_support.message(Command('catalog'))
async def catalog_cmd(message : types.Message):
    await message.answer('Ви бачете початок каталогу', reply_markup=reply_custom.catalog_kb)

@user_privat_router_support.message(or_f(Command('utk'),
                                        (F.text.lower().contains('тепло')),
                                        (F.text.lower().contains('вода')),
                                        (F.text.lower().contains('вентиля')),
                                        (F.text.lower().contains('електрик')),
                                        (F.text.lower().contains('провод')),
                                        (F.text.lower().contains('насос')),
                                        (F.text.lower().contains('котл')),
                                         ))
async def utk_cmd(message : types.Message):
    await message.answer('Вітаємо вас в УТК', reply_markup=reply_custom.utk2_kb.as_markup(
                                                        resize_keyboard=True,
                                                        input_field_placeholder='Що вас цікавить'
                                                        ))   


@user_privat_router_support.message(or_f(Command('doors'),
                                        (F.text.lower().contains('двер')),
                                        (F.text.lower().contains('шпалер')),
                                        (F.text.lower().contains('обои')),
                                        
                                         ))
async def doors_cmd(message : types.Message):
    await message.answer('Вітаємо вас в Маркеті Дверей', reply_markup=reply_custom.start_kb)       

@user_privat_router_support.message(F.text.lower().contains('вихід'))
@user_privat_router_support.message(Command('exit'))
async def exit_cmd(message : types.Message):
    await message.answer('До нових зустрічей 🖐️', reply_markup=reply_custom.del_kbd) 



@user_privat_router_support.message(F.text.lower().contains('резерв')) # ----------------- contains - шукає збіги у тексті повідомлення
async def filter_text_custom_two(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n з приводу резерву \n ви можете отримати відповіді за телефоном :\n {contact_consult}') 



@user_privat_router_support.message(F.text.lower().contains('консульт')) # ----------------- contains - шукає збіги у тексті повідомлення
async def filter_text_custom_three(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n можемо проконсультувати вас \n за телефоном :\n {contact_consult}')

@user_privat_router_support.message(F.text.lower().contains('замов')) # ----------------- contains - шукає збіги у тексті повідомлення
async def filter_text_custom_four(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n здійснити замолення ви можете \n за телефоном :\n {contact_consult}')    

@user_privat_router_support.message(F.text.lower().contains('монтаж')) # ----------------- contains - шукає збіги у тексті повідомлення
async def filter_text_custom_five(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n замовити монтаж  ви можете \n за телефоном :\n {contact_assembling}')

@user_privat_router_support.message(F.text.lower().contains('плат')) # ----------------- contains - шукає збіги у тексті повідомлення
async def filter_text_custom_six(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n здійснити оплату ви можете \n за телефоном :\n {contact_cashier}') 


