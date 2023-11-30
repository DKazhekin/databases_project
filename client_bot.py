import asyncio
import os
import asyncpg
import aiogram.utils.keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Dispatcher, Bot, types
from aiogram.filters.command import Command, Message
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


async def db_connection() -> asyncpg.connection.Connection:
    return await asyncpg.connect(
        user=os.getenv("BOT_USER"),
        password=os.getenv("BOT_PASSWORD"),
        database=os.getenv("BOT_DATABASE"),
        host=os.getenv("BOT_HOST")
    )


async def add_new_user(message: types.Message) -> None:
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT COUNT(*) FROM users WHERE user_id = $1", message.from_user.id
    )
    if data[0]['count'] == 0:
        await conn.execute(
            "INSERT INTO users (user_id, username, balance) VALUES($1, $2, $3)", message.from_user.id,
            message.from_user.username, 0
        )
    await conn.close()


async def get_balance(message: types.Message) -> list:
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT balance FROM users WHERE user_id=$1", message.from_user.id
    )
    await conn.close()
    return data


async def top_up_balance(message: types.Message, amount: int) -> None:
    conn = await db_connection()
    await conn.execute(
        "UPDATE users SET balance = balance + $2 WHERE user_id = $1", message.from_user.id, amount
    )
    await conn.close()


async def get_info(name: str) -> tuple:
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT price, country, url FROM products WHERE name = $1", str(name)
    )
    await conn.close()
    return data[0]['price'], data[0]['country'], data[0]['url']


async def add_2_cart(item: str, amount: int, id_: int) -> None:
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT COUNT(*) FROM cart WHERE user_id = $1 AND item_name = $2", id_, item
    )
    if data[0]['count'] == 0:
        await conn.execute(
            "INSERT INTO cart(user_id, item_name, item_count) VALUES ($1, $2, $3)", id_, item, amount
        )
    else:
        await conn.execute(
            "UPDATE cart SET item_count = item_count + $1 WHERE user_id = $2 AND item_name = $3", amount, id_, item
        )
    await conn.close()


# Start button
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Goods 📋")],
        [types.KeyboardButton(text="Account 🔑")],
        [types.KeyboardButton(text="Shopping Cart 🛒")],
        [types.KeyboardButton(text="History ⌛")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Hello! You are in the best telegram shop 🛍️! \n"
                         "Top up your balance in 'Account 🔑' \n"
                         "Make the first order through 'Goods 📋' \n"
                         "Check the history of your orders in 'History ⌛'", reply_markup=keyboard)

    await add_new_user(message)


@dp.message(F.text == "Account 🔑")
async def account_button(message: types.Message):
    top_up_button = types.KeyboardButton(text="Top Up Balance 💸")
    back_button_ = types.KeyboardButton(text="Back ⬅️")
    kb = [
        [top_up_button],
        [back_button_]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("     ACCOUNT \n"
                         "------------------ \n"
                         "Your ID 🪪 : {} \n"
                         "Your Username 👨🏻‍💻: @{} \n"
                         "Your Balance 💰 : {}$ \n".format(message.from_user.id, message.from_user.username,
                                                          (await get_balance(message))[0]['balance']),
                         reply_markup=keyboard)


@dp.message(F.text == "Shopping Cart 🛒")
async def cart_button(message: types.Message) -> None:
    keyboard = [
        [types.KeyboardButton(text="Back ⬅️")],
        [types.KeyboardButton(text="Clean Up Cart 🛒")],
        [types.KeyboardButton(text="Make Order ⭐")]
    ]
    kb = types.ReplyKeyboardMarkup(keyboard=keyboard)

    conn = await db_connection()
    data = await conn.fetch(
        "SELECT * FROM cart WHERE user_id = $1", message.from_user.id
    )
    output = "Your cart: \n\n"
    Summary = 0
    for record in data:
        if record['user_id'] == message.from_user.id:
            price_query = await conn.fetch(
                "SELECT price FROM products WHERE name = $1", record['item_name']
            )
            price = price_query[0]['price']
            line = "📦: {}    🏷️: {}$   🧮: x{}   📝:   {}$ \n".format(record['item_name'], round(price, 2),
                                                                    record['item_count'],
                                                                    round(price * record['item_count'], 2))
            output += line
            Summary += round(price * record['item_count'], 2)
    output += "\n" "Summary: " + str(Summary) + "$\n"
    await message.answer(text=output, reply_markup=kb)
    await conn.close()


@dp.message(F.text == "Clean Up Cart 🛒")
async def clean_up_cart_button(message: types.Message) -> None:
    conn = await db_connection()
    await conn.execute(
        "DELETE FROM cart WHERE user_id = $1", message.from_user.id
    )
    await conn.close()
    await cart_button(message)


@dp.message(F.text == "Make Order ⭐")
async def make_order(message: types.Message) -> None:
    conn = await db_connection()
    balance = await conn.fetch(
        "SELECT balance FROM users WHERE user_id = $1", message.from_user.id
    )

    cart = await conn.fetch(
        "SELECT * FROM cart WHERE user_id = $1", message.from_user.id
    )

    summary = 0
    # Считаем общую сумму заказа
    for record in cart:
        if record['user_id'] == message.from_user.id:
            price_query = await conn.fetch(
                "SELECT price FROM products WHERE name = $1", record['item_name']
            )
            price = price_query[0]['price']
            summary += round(price * record['item_count'], 2)

    # Если денег на балансе достаточно
    if balance[0]['balance'] >= summary:
        # Если корзина пуста
        if summary == 0:
            await message.answer(text="Please, add something to your cart to make the order 🙏 \n")
            return
        # Заполняем orders
        order_id = await conn.fetch(
            "INSERT INTO orders(creation_time) VALUES (CURRENT_TIMESTAMP) RETURNING order_id, creation_time"
        )
        # Заполняем order_body
        for record in cart:
            product_id = await conn.fetch(
                "SELECT product_id FROM products WHERE name = $1", record['item_name']
            )

            await conn.execute(
                "INSERT INTO order_body(order_id, product_id, counts) VALUES($1, $2, $3)", int(order_id[0]['order_id']),
                int(product_id[0]['product_id']),
                record['item_count']
            )
        await message.answer(text="Congratulations 🎉 \n"
                                  "You have made the order !\n"
                                  "Order id: {}".format(order_id[0]['order_id']))

        # Делаем запись в таблицу user_actions
        await conn.execute(
            "INSERT INTO user_actions(user_id, order_id, action, time) VALUES($1, $2, $3, $4)", message.from_user.id,
            int(order_id[0]['order_id']), 'create_order', order_id[0]['creation_time']
        )
        # Снимаем деньги с баланса
        await conn.execute(
            "UPDATE users SET balance = balance - $1 WHERE user_id = $2", summary, message.from_user.id
        )
    else:
        await message.answer(text="Unfortunately, you haven't got enough credits to make this purchase 😢\n"
                                  "Top up your balance in 'Account 🔑' \n")
    await conn.close()


@dp.message(F.text == "History ⌛")
async def history_button(message: types.Message) -> None:
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT * FROM user_actions WHERE user_id = $1", message.from_user.id
    )
    output = "History of your orders 📜: \n"
    for record in data:
        time = record['time']
        order_id = record['order_id']
        status = record['action']
        line = "🆔: {}    🕓: {}  Time: {} \n".format(order_id, status, time)
        output += line
    await message.answer(text=output)


@dp.message(F.text == "Back ⬅️")
async def back_button(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Goods 📋")],
        [types.KeyboardButton(text="Account 🔑")],
        [types.KeyboardButton(text="Shopping Cart 🛒")],
        [types.KeyboardButton(text="History ⌛")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text="You are in the main menu !", reply_markup=keyboard)


# Create FSM to display goods
class choose_button(StatesGroup):
    button = State()


@dp.message(F.text == "Goods 📋")
async def menu_button(message: types.Message, state: FSMContext):
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT * FROM products"
    )
    keyboard = [[InlineKeyboardButton(text=record['name'], callback_data=record['name'])] for record in data]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(text="Choose items you want to buy: 🛒", reply_markup=keyboard)
    await state.set_state(choose_button.button)
    await conn.close()


@dp.message(choose_button.button)
@dp.callback_query((F.data != "Back") & (F.data[:3] != "Add"))
async def query_buttons(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    price, country, url = await get_info(callback.data)
    bbutton = InlineKeyboardButton(text="Back ⬅️", callback_data="Back")
    add_button = InlineKeyboardButton(text="Add to cart ✏️", callback_data="Add:{}".format(callback.data))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[add_button], [bbutton]])
    await callback.message.answer_photo(
        photo=url,
        caption='Item: {} \n'
                'Price: {}$ \n'
                'Country: {} \n'.format(callback.data, round(price, 2), country),
        reply_markup=keyboard
    )
    await state.clear()


@dp.callback_query(F.data == "Back")
async def query_back_button(callback: types.CallbackQuery):
    await callback.message.delete()
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT * FROM products"
    )
    keyboard = [[InlineKeyboardButton(text=record['name'], callback_data=record['name'])] for record in data]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.answer(text="Choose items you want to buy: 🛒", reply_markup=keyboard)


# -----------------------------------
# Create FSM to handle amount of item in ordering state
class ItemAmount(StatesGroup):
    amount = State()


@dp.callback_query(F.data.split(sep=":")[0] == "Add")
async def add_2_cart_get_item(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(ItemAmount.amount)
    await state.update_data(item=callback.data.split(":")[1])
    await callback.message.answer(text="Enter the amount of items you want to order: 🙂")


@dp.message(ItemAmount.amount)
async def add_2_cart_take_quantity(message: types.Message, state: FSMContext):
    amount = message.text
    try:
        amount = int(amount)
        item_name = await state.get_data()
        await add_2_cart(item_name['item'], amount, message.from_user.id)
        await message.answer(text="Item has added to your cart ✅")
    except:
        await message.reply(text="Please provide correct number! ❌")
    finally:
        await state.clear()


# -----------------------------------

# ------------------------------------
# Create FSM to handle amount to top up
class TopUpBalance(StatesGroup):
    amount = State()


@dp.message(F.text == "Top Up Balance 💸")
async def top_up_balance_button(message: types.Message, state: FSMContext):
    await state.set_state(TopUpBalance.amount)
    await message.reply(text="Enter the amount you want to top up ! 💲")


@dp.message(TopUpBalance.amount)
async def balance_top_upped(message: types.Message, state: FSMContext):
    amount = message.text
    try:
        float(amount)
        await top_up_balance(message, int(amount))
        await message.answer(text="Balance is topped up correctly ✅")
    except ValueError:
        await message.reply(text="Please provide correct number to top up! ❌")
    finally:
        await state.clear()


# ------------------------------------


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
