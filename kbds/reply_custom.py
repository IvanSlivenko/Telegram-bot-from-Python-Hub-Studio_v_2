from  aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Каталог 🚪"),
            
        ],
        [
            KeyboardButton(text="Про нас 📖"),
            KeyboardButton(text="Монтаж 🛠️"),
            KeyboardButton(text="Варіанти доставки 🚐"),
            KeyboardButton(text="Оплата 💰"),
            
        ],
        [
            KeyboardButton(text="Відправити номер  ☎", request_contact=True),
            KeyboardButton(text="Віправити локацію 🌍", request_location= True),
            KeyboardButton(text="Створити опитування 🎤", request_poll=KeyboardButtonPollType())
        ],
         [
            KeyboardButton(text="Вихід 🏡"),
            
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
        )

utk_kb.adjust(3)

utk2_kb=ReplyKeyboardBuilder()
utk2_kb.attach(utk_kb) 
utk2_kb.row(KeyboardButton(text="Монтаж"),  
            KeyboardButton(text="Доставка"),
            KeyboardButton(text="Вихід"),)
