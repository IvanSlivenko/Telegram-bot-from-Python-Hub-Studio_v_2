from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from database.models import Product


# --------------------------- Cтворюємо продукт
async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        kode=data["kode"],
        image=data["image"],
    )  # --------------------------------------- Готуємо запис для бази данних

    session.add(obj)  # ------------------------ Записуємо запис в базу данних
    await session.commit()  # -------------------- Фіксуємо запис в базі данних


# ------------------------- Отимуємо список всіх продуктів
async def orm_get_products(session: AsyncSession):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()


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
        )
    )
    await session.execute(query)
    await session.commit()


# ------------------------------ Видаляємо продукт
async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()
