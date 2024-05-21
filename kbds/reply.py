from  aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
                *btns: str,
                placeholder: str=None,
                request_contact:int=None, #--- передаємо індекс цієї кнопки в списку кнопок
                request_location:int=None, #--- передаємо індекс цієї кнопки в списку кнопок
                sizes:tuple[int]=(2,)

                ):
    
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
     
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))        


    return keyboard.adjust(*sizes).as_markup(
                                                resize_keyboard=True,
                                                input_field_placeholder=placeholder
                                            )   

    

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="Про нас"), 
        ],
        [
            KeyboardButton(text="Варіанти доставки"),
            KeyboardButton(text="Варіанти оплати"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Що вас цікавить ?'
)

del_kbd = ReplyKeyboardRemove()

start_kb_2 = ReplyKeyboardBuilder()
start_kb_2.add(
            KeyboardButton(text="Меню"),
            KeyboardButton(text="Про нас"), 
            KeyboardButton(text="Варіанти доставки"),
            KeyboardButton(text="Варіанти оплати"),       
        )

start_kb_2.adjust(2,2)


start_kb_3 = ReplyKeyboardBuilder()
start_kb_3.attach(start_kb_2)
start_kb_3.row(KeyboardButton(text="Відгук"),) # ------ row додає новим  рядком


test_kb= ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Створити опитування", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text="Відправити номер ☎", request_contact=True),
            KeyboardButton(text="Віправити локацію 🌍", request_location= True),
        ],
    ],
    resize_keyboard=True)