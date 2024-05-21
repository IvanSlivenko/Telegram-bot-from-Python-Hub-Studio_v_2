from string import punctuation

from aiogram import F, Bot, types, Router
from aiogram.filters import CommandStart, Command, or_f

from common.registred_words import registred_words
from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group','supergroup']))
user_group_router.edited_message.filter(ChatTypeFilter(['group','supergroup']))

@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot=Bot):
    chat_id = message.chat.id
    admins_list= await bot.get_chat_administrators(chat_id)
    # print(admins_list)

    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ] 

    bot.my_admins_list = admins_list 
    if message.from_user.id in admins_list:
        await message.delete()
        await message.answer(f'Вітаємо.\n{message.from_user.first_name}\n ви активувались у групі,\n як Aдміністратор')



def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation)) # ----------------------------- delete liter punctuation

@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if registred_words.intersection(clean_text(message.text.lower()).split()): # ----------------split() create {}
        await message.answer(f'{message.from_user.first_name} Прохання слідкувати за культурою комунікації')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
    else:
        await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n Ваш запит :\n "{message.text}"\n ще не зрозумілий для нашої системи ')    
        




         