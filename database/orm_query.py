import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload

from database.models import Product , Banner , Cart, Category, User

# # Простий пагінатор
# class Paginator:
#     def __init__(self, array: list | tuple, page:int=1, per_page: int=1 ) -> None:
#         self.array = array
#         self.per_page = per_page
#         self.page = page
#         self.len = len(self.array)
#         self.pages = math.ceil(self.len / self.per_page)

#     def __get_slise(self):
#         start = (self.page - 1)*self.per_page
#         stop = start + self.per_page
#         return self.array[start:stop]
    
#     def get_page(self):
#         page_items = self.__get_slise()
#         return page_items
    
#     def has_next(self):
#         if self.page < self.pages:
#             return self.page + 1
#         return False
    
#     def has_previous(self):
#         if self.page > 1:
#             return self.page - 1
#         return False

#     def get_next(self):
#         if self.page < self.pages:
#             self.page += 1
#             return self.get_page()
#         raise IndexError(f'Next page does not exist. Use has_next() to check before.')

#     def get_previous(self):
#         if self.page > 1:
#             self.page -= 1
#             return self.__get_slise()
#         raise IndexError(f'Previous page does not exist. Use has_previous() to check before.')
        
    
    #------------------------------------------------ Робота з банерами (інформаційними сторінками)

async def orm_add_banner_description(session: AsyncSession, data: dict):
    #Добавляем новый или изменяем существующий по именам
    #пунктов меню: main, about, cart, shipping, payment, catalog
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description=description) for name, description in data.items()]) 
    await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()
   

async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()


#------------------------------------------------- Категорії

async def orm_get_categories(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_category(session: AsyncSession, category_id: int):
    query = select(Category).where(Category.id == category_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories]) 
    await session.commit()    






# --------------------------- Cтворюємо продукт
async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        kode=data["kode"],
        image=data["image"],
        category_id=int(data["category"]),
    )  # --------------------------------------- Готуємо запис для бази данних

    session.add(obj)  # ------------------------ Записуємо запис в базу данних
    await session.commit()  # -------------------- Фіксуємо запис в базі данних

# ------------------------- Отимуємо список всіх продуктів
async def orm_get_products_all(session: AsyncSession):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()

# ------------------------- Отимуємо список всіх продуктів по категорії
async def orm_get_products(session: AsyncSession, category_id: int):
    query = select(Product).where(Product.category_id == int(category_id))
    result = await session.execute(query)
    return result.scalars().all()
#------------------------------------------------------------------??????????????????????????
# ------------------------- Отимуємо список всіх продуктів по коду
async def orm_get_products_with_kode(session: AsyncSession, product_kode: int):
    query = select(Product).where(Product.kode == product_kode)
    result = await session.execute(query)
    return result.scalars().all()
#-----------------------------------------------------------------???????????????????????????

# ------------------------- Отимуємо один продукт
async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar()


# --------------------------Змінюємо продукт
async def orm_update_product(session: AsyncSession, product_id: int, data):
    query = (
        update(Product)
        .where(Product.id == product_id)
        .values(
            name=data["name"],
            description=data["description"],
            price=float(data["price"]),
            kode=data["kode"],
            image=data["image"],
            category_id=int(data["category"]),
        )
    )
    await session.execute(query)
    await session.commit()


# ------------------------------ Видаляємо продукт
async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()

#---------------------------------------------------------------------Робота з Юзерами

async def orm_add_user(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        ):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, first_name=first_name, last_name=last_name, phone=phone)
        )
        await session.commit()


#--------------------------------------------------------------------- Робота з корзинами

async def orm_add_to_cart(session: AsyncSession, user_id: int, product_id: int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).options(joinedload(Cart.product))
    cart = await session.execute(query)
    cart = cart.scalar()
    if cart:
        cart.quantity += 1
        await session.commit()
        return cart
    else:
        session.add(Cart(user_id=user_id, product_id=product_id, quantity=1))
        await session.commit()



async def orm_get_user_carts(session: AsyncSession, user_id):
    query = select(Cart).filter(Cart.user_id == user_id).options(joinedload(Cart.product))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_from_cart(session: AsyncSession, user_id: int, product_id: int):
    query = delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    await session.execute(query)
    await session.commit()


async def orm_reduce_product_in_cart(session: AsyncSession, user_id: int, product_id: int):
    # query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).options(joinedload(Cart.product))
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    cart = await session.execute(query)
    cart = cart.scalar()

    if not cart:
        return
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await orm_delete_from_cart(session, user_id, product_id)
        await session.commit()
        return False    
