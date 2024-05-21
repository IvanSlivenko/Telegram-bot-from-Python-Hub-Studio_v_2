from aiogram import F, Router, types
from aiogram.filters import Command, or_f

from filters.chat_types import ChatTypeFilter, IsAdmin

from kbds.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB=get_keyboard(
                        'Додати товар',
                        'Змінити товар',
                        'Видалити товар',
                        'Переглянути товари',
                        placeholder='Оберіг дію',
                        sizes=(2,1,1)

                    )

@admin_router.message(or_f(
                            (Command("admin")),
                            (F.text.lower().contains('адмін')),
                          )
                    )
async def admin_access(message: types.Message):
    await message.answer('Що будемо робити', reply_markup=ADMIN_KB)

@admin_router.message(F.text.lower() =='переглянути товари') 
async def starring_at_product(message: types.Message):
    await message.answer('Тут буде список товарів')

@admin_router.message(F.text.lower() =='змінити товар') 
async def change_product(message: types.Message):
    await message.answer('Тут будемо змінювати товар')       

@admin_router.message(F.text.lower() =='видалити товар') 
async def delete_product(message: types.Message):
    await message.answer('Тут будемо видаляти товар')

#-------------------------------------------------------Машина Стану ( FSM )

@admin_router.message(F.text.lower() =='додати товар') 
async def add_product(message: types.Message):
    await message.answer('Вкажіть назву товару', reply_markup=types.ReplyKeyboardRemove())

@admin_router.message(Command("відміна"))
@admin_router.message(F.text.casefold() == "відміна") # ---------------casefold()    повертає стрічку у нижньому реєстрі
async def cancel_handler(message:types.Message) -> None:
    await  message.answer('Дії відмінені', reply_markup=ADMIN_KB)

@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад") # ---------------casefold()    повертає стрічку у нижньому реєстрі
async def reverse_handler(message:types.Message) -> None:
    await  message.answer('Ви повернулись до попередього кроку')

@admin_router.message(F.text)
async def add_name(message: types.Message):
    await message.answer('Вкажіть опис товару')

@admin_router.message(F.text)
async def add_description(message: types.Message):
    await message.answer('Вкажіть ціну товару')

@admin_router.message(F.text)
async def add_price(message: types.Message):
    await message.answer('Додайте фото товару')

@admin_router.message(F.photo)
async def add_image(message: types.Message):
    await message.answer('Товар додано', reply_markup=ADMIN_KB)             







