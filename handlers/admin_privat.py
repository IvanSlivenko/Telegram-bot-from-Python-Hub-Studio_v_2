from aiogram import F, Router, types
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard
from database.orm_query import  orm_add_product,\
                                orm_get_product, \
                                orm_get_products, \
                                orm_update_product,\
                                orm_delete_product

from kbds.inline import get_callback_btns


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
    "Додати товар",
    "Асортимент для редагування",
    placeholder="Оберіть дію",
    sizes=(2,),
)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    kode = State()
    image = State()

    product_fo_change= None

    texts = {
        "AddProduct:name": "Введіть назву знову",
        "AddProduct:description": "Введіть опис знову",
        "AddProduct:price": "Введіть ціну знову",
        "AddProduct:kode": "Введіть  код знову ",
        "AddProduct:image": "Цей стейт останній ",
    }
    


@admin_router.message(
    or_f(
        (Command("admin")),
        (F.text.lower().contains("адмін")),
        (F.text.lower().contains("//")),
        (F.text.lower().contains("\\")),
    )
)
async def admin_access(message: types.Message):
    await message.answer("Що будемо робити", reply_markup=ADMIN_KB)


@admin_router.message(F.text.lower() == "асортимент для редагування")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\n</strong>\n \
                Код: {product.kode}\n \
                {product.description}\n \
                Ціна: {round(product.price, 2)}",
                reply_markup=get_callback_btns(
                    btns={
                          'Bидалити':f'delete_{product.id}',
                          'Редагувати':f'change_{product.id}'  
                    })
                )

#------------------------------------------ CallbackQuery--------------

@admin_router.callback_query(F.data.startswith("delete_")) #----startswith починається з 
async def delete_product(callback:types.CallbackQuery, session: AsyncSession):


    product_id= callback.data.split("_")[-1]

    curent_product=await orm_get_product(session, int(product_id))
    await orm_delete_product(session, int(product_id))

    await callback.answer('Товар видалено')#----------- Повідомлення для серверів Телеграму
    await callback.message.answer(f'Товар {curent_product.name} видалено')#--------- Повідомлення для користувача
    

@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(callback:types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    product_fo_change = await orm_get_product(session, int(product_id))

    AddProduct.product_fo_change = product_fo_change

    await callback.answer()
    await callback.message.answer(
        "Вкажіть назву товара ", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)#---------------------------------- стаємо в стан зміни назви продукту



# -------------------------------------------------------Машина Стану ( FSM )


@admin_router.message(
    StateFilter(None), F.text.lower() == "додати товар"
)  # ----------------StateFilter(None) перевіряє вдсутність активних станів
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Вкажіть назву товару", reply_markup=types.ReplyKeyboardRemove()
    )
    # ------------------- Стаємо в стан очікування в стадію "name"
    await state.set_state(AddProduct.name)


# ======================================================================================
@admin_router.message(StateFilter("*"), Command("відміна"))
@admin_router.message(
    StateFilter("*"), F.text.casefold() == "відміна"
)  # ---------------casefold()    повертає стрічку у нижньому реєстрі
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    curretnt_state = await state.get_state()
    if curretnt_state is None:
        return

    await state.clear()
    await message.answer("Дії відмінені", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter("*"), Command("назад"))
@admin_router.message(
    StateFilter("*"), F.text.casefold() == "назад"
)  # ---------------casefold()    повертає стрічку у нижньому реєстрі
async def reverse_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer(
            "Попереднього кроку нема, вкажіть назву товару або напишіть відміна "
        )
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ви повернулись до попередього кроку\n {AddProduct.texts[previous.state]}"
            )
            return
        previous = step


# =======================================================================================


# ------------------------------------------- state ==  name
@admin_router.message(
    AddProduct.name, or_f((F.text),(F.text == ".")) 
)  # ------------------------------------- AddProduct.name перевіряє чи ми у стейті name
async def add_name(message: types.Message, state: FSMContext):

    #---------------------------------------------------------------------------------
    # fild_test=None
    # if message.text == ".":
    #     await state.update_data(fild_test=AddProduct.product_fo_change.fild_test)
    # else:
    #---------------------------------------------------------------------------------

    if message.text == ".":
        await state.update_data(name=AddProduct.product_fo_change.name)
    else:
        if len(message.text) >= 100:
            await message.answer("Назва товара не повинна перевищувати 100 символів\n Вкажіть назву знову")
            return
        
        await state.update_data(
        name=message.text
    )  # ---------------------- фіксуємо в state назву товару

    await message.answer("Вкажіть опис товару")
    await state.set_state(
        AddProduct.description)  # ---------------Переходимо в state == description


@admin_router.message(
    AddProduct.name
)  # ------------------------------------- AddProduct.name перевіряє чи ми у стейті name
async def add_name_error(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели не допустимі данні")


# -------------------------------------------------------------------------------------------------------------
# ------------------------------------------- state ==  description
@admin_router.message(AddProduct.description, or_f((F.text),(F.text == ".")))
async def add_description(message: types.Message, state: FSMContext):

    if message.text == ".":
        await state.update_data(description=AddProduct.product_fo_change.description)
    else:
        await state.update_data(
            description=message.text
        )  # ---------------------- фіксуємо в state
    await message.answer("Вкажіть ціну товару")
    await state.set_state(AddProduct.price)


@admin_router.message(
    AddProduct.description
)  # ------------------------------------- AddProduct.name перевіряє чи ми у стейті name
async def add_description_error(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели не допустимі данні")


# ------------------------------------------- state ==  price
@admin_router.message(AddProduct.price, or_f((F.text),(F.text == ".")))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(price=AddProduct.product_fo_change.price)
    else:
        await state.update_data(
            price=message.text
        )  # ---------------------- фіксуємо в state
    await message.answer("Вкажіть внутрішній код товару")
    await state.set_state(AddProduct.kode)


@admin_router.message(
    AddProduct.price
)  # ------------------------------------- AddProduct.name перевіряє чи ми у стейті name
async def add_price_error(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели не допустимі данні")


# ------------------------------------------- state ==  kode
@admin_router.message(AddProduct.kode, F.text)
async def add_artikle(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(kode=AddProduct.product_fo_change.kode)
    else:
        await state.update_data(
            kode=message.text
        )  # ---------------------- фіксуємо в state
    await message.answer("Додайте фото товару")
    await state.set_state(AddProduct.image)


@admin_router.message(
    AddProduct.kode
)  # ------------------------------------- AddProduct.name перевіряє чи ми у стейті name
async def add_kode_error(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели не допустимі данні")


@admin_router.message(AddProduct.image, or_f((F.text),(F.text == "."), (F.photo)))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == ".":
        await state.update_data(image=AddProduct.product_fo_change.image)
    else:
        await state.update_data(
            image=message.photo[-1].file_id
        )  # ---------------------- фіксуємо в state photo == max id
        data = (
            await state.get_data()
        )  # ------------------------------- зберігаємо state в змінну data
    try:
        await orm_add_product(session, data)
        await message.answer(f"Товар {data['name']} додано", reply_markup=ADMIN_KB)
        await state.clear()  # ------------------------------------------- очищаємо state
    except Exception as e:
        await message.answer(
            f"Помилка: \n {str(e)}\n зверніться до розробника ", reply_markup=ADMIN_KB
        )

        await state.clear()  # ------------------------------------------- очищаємо state


@admin_router.message(
    AddProduct.image
)  # ------------------------------------- AddProduct.name перевіряє чи ми у стейті name
async def add_image_error(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели не допустимі данні")


#===========================================================================
# @admin_router.message(F.text.lower() == "змінити товар")
# async def change_product(message: types.Message):
#     await message.answer("Тут будемо змінювати товар")


# @admin_router.message(F.text.lower() == "видалити товар")
# # async def delete_product(message: types.Message, counter):
# async def delete_product(message: types.Message):
#     # await message.answer(f'counter: {counter}')
#     await message.answer("Тут будемо видаляти товар")
#============================================================================