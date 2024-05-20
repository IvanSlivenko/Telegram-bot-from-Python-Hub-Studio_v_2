from  aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Каталог"),
            
        ],
        [
            KeyboardButton(text="Про нас"),
            KeyboardButton(text="Монтаж"),
            KeyboardButton(text="Варіанти доставки"),
            KeyboardButton(text="Оплата"),
            
        ],
        [
            KeyboardButton(text="Вихід"),
            
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Що вас цікавить у Маркеті Дверей ?'
)


catalog_kb = ReplyKeyboardMarkup(
    keyboard=[
        
        [
            KeyboardButton(text="Зовнішні"),
            KeyboardButton(text="Внутрішні"),

            
        ],
        [
            KeyboardButton(text="Замір"),
            KeyboardButton(text="Монтаж"),
            
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Що вас цікавить у Маркеті Дверей ?'
)

del_kbd = ReplyKeyboardRemove()


#-------------------------------------------------

utk_kb = ReplyKeyboardBuilder()
utk_kb.add(   
            KeyboardButton(text="Опалення"),
            KeyboardButton(text="Водопостачання"),
            KeyboardButton(text="Електротовари"),
            KeyboardButton(text="Монтаж"),           
        )

utk_kb.adjust(3,1)

utk2_kb=ReplyKeyboardBuilder()
utk2_kb.attach(utk_kb)
utk2_kb.row(KeyboardButton(text="Доставка"),
            KeyboardButton(text="Вихід"),)
