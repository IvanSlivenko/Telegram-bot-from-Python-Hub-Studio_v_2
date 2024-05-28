from aiogram.utils.formatting import as_list, as_marked_section, Bold

categories = [
    'внутрішні',
    'зовнішні'
]

description_for_info_pages = {
    "main":"Вітаємо",
    "about":"Маркет Дверей\n Режим роботи\n",
    "payment": as_marked_section(
                                Bold("Варіанти оплати"),
                                "Готівка",
                                "Банківський рахунок",
                                "Кредитна Картка",
                                marker="💰",
                            ).as_html(),
    "shipping": as_marked_section(
                            Bold("Варіанти доставки"),
                            "Власний транспорт",
                            "Транспорт третіх осіб",
                            marker="🚙",
                        ).as_html(),
    'catalog':'Категорії',
    'cart': 'Корзина пуста',
    'reserve': 'резерв',

}