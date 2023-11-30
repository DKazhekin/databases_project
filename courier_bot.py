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

bot = Bot(token=os.getenv("BOT_COURIER_TOKEN"))
dp = Dispatcher()


async def db_connection() -> asyncpg.connection.Connection:
    return await asyncpg.connect(
        user=os.getenv("BOT_USER"),
        password=os.getenv("BOT_PASSWORD"),
        database=os.getenv("BOT_DATABASE"),
        host=os.getenv("BOT_HOST")
    )


async def get_inprocess_action_courier(message: types.Message) -> list:
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT order_id FROM courier_actions WHERE courier_id = $1 AND action = $2", message.from_user.id, 'in_process'
    )
    await conn.close()
    return data


async def get_available_deliveries(message: types.Message) -> list:
    conn = await db_connection()
    data = await conn.fetch(
        "SELECT order_id FROM user_actions WHERE action = $1", 'create_order'
    )
    await conn.close()
    return data


@dp.message(F.text == "Current Deliveries")
async def current_deliveries_button(message: types.Message):
    data_list = await get_inprocess_action_courier(message)
    data_list = [str(i) for i in data_list]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=data, callback_data="button2:" + data)] for data in data_list
    ])
    await message.answer("Current deliveries:\n",

                         reply_markup=keyboard
                         )


@dp.callback_query(lambda c: c.data.startswith('button2:'))
async def available_deliveries_button_callback(callback_query: types.CallbackQuery):
    conn = await db_connection()
    await conn.execute("UPDATE user_actions SET action = 'delivered', time = CURRENT_TIMESTAMP WHERE order_id = $1",
                       int(callback_query.data[25:-1]))
    await conn.execute("UPDATE courier_actions SET action = 'delivered', time = CURRENT_TIMESTAMP WHERE order_id = $1",
                       int(callback_query.data[25:-1]))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "You delivered the order!")




@dp.message(F.text == "Available Deliveries")
async def available_deliveries_button(message: types.Message):
    data_list = await get_available_deliveries(message)
    data_list = [str(i) for i in data_list]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=data, callback_data="button1:" + data)] for data in data_list
    ])
    await message.answer("Available deliveries:\n",

                         reply_markup=keyboard
                         )


@dp.callback_query(lambda c: c.data.startswith('button1:'))
async def available_deliveries_button_callback(callback_query: types.CallbackQuery):
    conn = await db_connection()
    await conn.execute("UPDATE user_actions SET action = 'in_process', time = CURRENT_TIMESTAMP WHERE order_id = $1",
                       int(callback_query.data[25:-1]))
    await conn.execute(
        "INSERT INTO courier_actions (courier_id, order_id, action, time) VALUES ($1, $2, 'in_process', CURRENT_TIMESTAMP)",
        callback_query.from_user.id, int(callback_query.data[25:-1]))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Now it's your order !")


@dp.message(F.text == "Courier Account 🔑")
async def account_button(message: types.Message):
    back_button_ = types.KeyboardButton(text="Back ⬅️")
    current_deliveries_button_ = types.KeyboardButton(text="Current Deliveries")
    available_deliveries_button_ = types.KeyboardButton(text="Available Deliveries")
    kb = [
        [current_deliveries_button_],
        [available_deliveries_button_],
        [back_button_]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Courier ACCOUNT \n"
                         "------------------ \n"
                         "Your ID 🪪 : {} \n".format(message.from_user.id),
                         reply_markup=keyboard)


@dp.message(F.text == "Back ⬅️")
async def back_button(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Courier Account 🔑")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text="You are in the main menu !", reply_markup=keyboard)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [[types.KeyboardButton(text="Courier Account 🔑")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Hello, you are in the courier menu !", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
