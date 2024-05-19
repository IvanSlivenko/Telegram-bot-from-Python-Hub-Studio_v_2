
from aiogram import F, types,  Router
from aiogram.filters import CommandStart, Command

from common.contacts_list import contact_shipping, contact_consult
from filters.chat_types import ChatTypeFilter

user_privat_router_support = Router()
user_privat_router_support.message.filter(ChatTypeFilter(['private']))





@user_privat_router_support.message(F.text.lower().contains('резерв')) # ----------------- contains - шукає збіги у тексті повідомлення
async def filter_text_custom_two(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n з приводу резерву \n ви можете отримати відповіді за телефоном :\n {contact_consult}') 



@user_privat_router_support.message(F.text.lower().contains('консульт')) # ----------------- contains - шукає збіги у тексті повідомлення
async def filter_text_custom_three(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n можемо проконсультувати вас \n за телефоном :\n {contact_consult}')

@user_privat_router_support.message(F.text.lower().contains('замов')) # ----------------- contains - шукає збіги у тексті повідомлення
async def filter_text_custom_four(message : types.Message):
    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n здійснити замолення ви можете \n за телефоном :\n {contact_consult}')                    


