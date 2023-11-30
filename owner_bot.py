import asyncio
import os
import asyncpg
import logging
import aiogram.utils.keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Dispatcher, Bot, types
from aiogram.filters.command import Command, Message
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime

bot = Bot(token=os.getenv("BOT_OWNER_TOKEN"))
dp = Dispatcher()


async def db_connection() -> asyncpg.connection.Connection:
    return await asyncpg.connect(
        user=os.getenv("BOT_USER"),
        password=os.getenv("BOT_PASSWORD"),
        database=os.getenv("BOT_DATABASE"),
        host=os.getenv("BOT_HOST")
    )


# Start button
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Metrics 📈")],
        [types.KeyboardButton(text="Add 🔔")],
        [types.KeyboardButton(text="List 📜")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Hello! Welcome to your account 🎉\n\n"
                         "You can get metrics using 'Metrics 📈' button \n"
                         "Add some items to your shop with 'Add item 🔔' button \n"
                         "Check what items are on sale with 'List 📜' button \n", reply_markup=keyboard)


@dp.message(F.text == "Metrics 📈")
async def metrics_button(message: types.Message):
    conn = await db_connection()
    revenue = (await conn.fetch(
        "SELECT SUM(ROUND((counts * price)::DECIMAL, 2)) AS revenue FROM orders INNER JOIN order_body USING(order_id) INNER JOIN products USING(product_id)"
    ))[0]['revenue']

    orders_count = (await conn.fetch(
        "SELECT COUNT(*) FROM orders"
    ))[0]['count']

    best_user = (await conn.fetch(
        "WITH group_ AS (SELECT user_id, COUNT(*) AS count_order FROM user_actions GROUP BY user_id) SELECT * FROM group_ INNER JOIN users USING(user_id) WHERE count_order = (SELECT MAX(count_order) FROM group_)"
    ))[0]

    text = ("💸 Your current revenue is: {}$ \n"
            "#️⃣ Total orders count is: {} \n"
            "👤 The most active user: @{} with {} orders !").format(revenue, orders_count, best_user['username'],
                                                                   best_user['count_order'])

    await message.answer(text=text)
    await conn.close()


@dp.message(F.text == "List 📜")
async def list_items_button(message: types.Message):
    text = ""
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT * FROM products"
    )
    for record in data:
        item_name = record['name']
        price = record['price']
        line = "🏷: {}  - 💰: {} \n".format(item_name, round(price, 2))
        text += line

    await message.answer(text=text)
    await conn.close()


# Crate FSM to validate information about new item
# ------------------------------------
class add_item(StatesGroup):
    item_name = State()
    price = State()
    url = State()
    country = State()


@dp.message(F.text == "Add 🔔")
async def add_item_button(message: types.Message, state: FSMContext):
    await state.set_state(add_item.item_name)
    await message.answer(text="Please provide the new item's name:")


@dp.message(add_item.item_name)
async def item_name_input(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(add_item.price)
    await message.answer("Good! Provide the price of this item please:")


@dp.message(add_item.price)
async def item_price_input(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(add_item.url)
    await message.answer("Cool! We need url of the image:")


@dp.message(add_item.url)
async def item_url_input(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(add_item.country)
    await message.answer("Well! Provide the country of your item:")


@dp.message(add_item.country)
async def item_country_input(message: types.Message, state: FSMContext):
    saved_data = await state.get_data()
    conn = await db_connection()
    await conn.execute(
        "INSERT INTO products(name, price, url, country) VALUES($1, $2, $3, $4)", saved_data['name'],
        round(float(saved_data['price']), 2), saved_data['url'], message.text
    )
    await message.answer(text="Success! Item has been added ✅")
    await conn.close()
# ---------------------------------------


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
