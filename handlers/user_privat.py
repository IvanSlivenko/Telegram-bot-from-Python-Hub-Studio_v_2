
from aiogram import F, types,  Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from common.contacts_list import contact_shipping
from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from database.orm_query import orm_add_user, orm_add_to_cart, orm_get_product


from kbds import reply
from kbds import reply_custom

from kbds.reply import get_keyboard
from kbds.inline import get_callback_btns, MenuCallBack


user_privat_router = Router()
user_privat_router.message.filter(ChatTypeFilter(['private']))


#------------------------------------------------------------- test 1
@user_privat_router.message(F.text == 'test')
async def test_cmd(mesage:types.Message):
    await mesage.answer('Тут ми тестуємо нову функцію', reply_markup=get_callback_btns(btns={
                                                    'Натисніть мене ': 'test_1'
                                                    }))
    
@user_privat_router.callback_query(F.data.startswith('test_'))
async def test_counter(callback: types.CallbackQuery):
    number = int(callback.data.split("_")[-1])

    await callback.message.edit_text(
        text=f"Натиснутий - {number}",
        reply_markup=get_callback_btns(btns={
                                     'Натисніть ще раз': f'test_{number+1}',

                                     }))
    




#-------------------------------------------------------------- test 1

#-------------------------------------------------------------Команда /sectors
@user_privat_router.message(
        or_f(
            Command('sectors'), 
            (F.text.lower().contains('сектор')),
            (F.text.lower().contains('відділ')),
            (F.text.lower().contains('підрозділ')),
            (F.text.lower().contains('будматеріали')),
            )
        )
async def sectors_cmd(message: types.Message):
    await message.answer(f'Привіт.  {message.from_user.first_name}.  Вам доступні такі підрозділи',
                         reply_markup=get_keyboard(
                                                    'Покрівля та фасад 🏠',    
                                                    'Буд матеріали 🏘️',
                                                    'Умань Тепло Комфорт 🚰',
                                                    'Вікна 🌬️',
                                                    'Двері 🚪',
                                                    placeholder='Оберіть підрозділ',
                                                    sizes=(1,2,2)                          
                                                    ),

                        )


#------------------------------------------------------------ Команда /start
@user_privat_router.message(CommandStart())
@user_privat_router.message(
        or_f( 
            (F.text.lower().contains('дивитись')),
            )
        )
async def start_cmd(message : types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")
    
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)

#----------------------------------------------Cart
async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):

    current_product_id=callback_data.product_id
    current_product = await orm_get_product(session, int(current_product_id))
    
    # user = callback.from_user
    current_user_id=int(callback.from_user.id)
    
    await orm_add_user(
        session,
        user_id=current_user_id,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name,
        phone=None,
    )


    await orm_add_to_cart(session, user_id=current_user_id, product_id=callback_data.product_id)
    await callback.answer(f"Товар : '{current_product.name}' додано в корзину", show_alert=True)
    # await callback.answer(f"Товар {current_product.name} додано в корзину")

#--------------------------------------------------------------------------
 

@user_privat_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    
    if callback_data.menu_name == "add_to_cart":
        await add_to_cart(callback, callback_data, session)
        return
  

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page = callback_data.page,
        user_id = callback.from_user.id,
        
    )

    

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()



    





#-------------------------------------------------------------------------------- Команда /start
# @user_privat_router.message(CommandStart())
# async def start_cmd(message : types.Message):
    
    
#     await message.answer("Привіт, я віртуальний помічник",
#                          reply_markup=get_callback_btns(btns={
#                              'Натисни менe': 'some_1'
#                          }))
    
# @user_privat_router.callback_query(F.data.startswith('some_'))
# async def counter(callback: types.CallbackQuery):
#     number = int(callback.data.split('_')[-1])

#     await callback.message.edit_text(
#         text=f"Натиснуто - {number}",
#         reply_markup=get_callback_btns(btns={
#                              'Додати 1 ':f'some_{number+1}',
#                              'Відняти 1 ':f'some_{number-1}',
#                          }))

#--------------------------------------------------------------------------------
    
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
async def menu_cmd(message : types.Message):
    await message.answer(f'{message.from_user.first_name}  ви викликали команду меню', reply_markup=reply.del_kbd)
    

@user_privat_router.message(F.text.lower().contains('про нас'))
@user_privat_router.message(Command('about'))
async def about_cmd(message : types.Message):
    await message.answer('Про нас')

@user_privat_router.message(or_f((Command('payment')),
                                 (F.text.lower().contains('заплат')), 
                                 (F.text.lower().contains('оплат')), 
                                 (F.text.lower() == 'оплата'),
                                 )
                            )

async def payment_cmd(message : types.Message):
    text = as_marked_section(
        Bold('Варіанти оплати :\n'),
        'Банківський рахунок',
        'Готівка',
        'Кредитна Картка',
        marker='✅'

        
    )
    await message.answer(text.as_html())
   

@user_privat_router.message(or_f((Command('shipping')),
                                 (F.text.lower().contains('привез')),  
                                 (F.text.lower().contains('достав')),
                                 (F.text.lower() == 'варіанти доставки'),
                                 )
                            ) # ----------------- contains - шукає збіги у тексті повідомлення

async def filter_text_custom_contains(message : types.Message):
    text = as_list(
        as_marked_section(
            Bold('Варіанти доставки :\n'),
            'Наш траспорт',
            'Траспорт третіх осіб',
            'Самовивіз',
        marker='✅'),
        as_marked_section(
            Bold('Доставка не відбувається :\n'),
            'На велосипеді',
            'На скутері',
            'На гелікоптері',
        marker='👉'),
        sep='\n-------------------\n'
    )
    
    await message.answer(text.as_html())
         

@user_privat_router.message(F.text) #------------------------------------------ Текстовий фільтр розташовуємо після всіх  конструкцій
async def filter_text_some(message : types.Message):

    await message.answer(f'Вітаємо.\n {message.from_user.first_name}\n Ваш запит :\n "{message.text}"\n ще не зрозумілий для нашої системи ')         

@user_privat_router.message(F.contact) #----------------------- ловимо контакт
async def get_contact(message: types.Message):
    await message.answer(f'Контакт отримано :\n{str(message.contact)}')
    await message.answer(f' номер отримано :\n{str(message.contact.phone_number)}')

@user_privat_router.message(F.location)#----------------------- ловимо  локацію
async def get_location(message: types.Message):
    await message.answer(f'локацію отримано {str(message.location)}')        


#--------------------------------------------------------------------------------------------   
    # await message.answer(f'Привіт.  {message.from_user.first_name}.  Я віртуальний помічник',
    #                      reply_markup=reply.start_kb_3.as_markup(
    #                          resize_keyboard=True,
    #                          input_field_placeholder='Що вас цікавить'
    #                         )
    #                      )
#--------------------------------------------------------------------------------------------

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
