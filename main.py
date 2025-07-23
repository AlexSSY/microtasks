import os
import sys
import logging
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart


dp = Dispatcher()


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def menu_reply_keyboard():
    buttons = [
        [KeyboardButton(text="Tasks"), KeyboardButton(text="Add Task")],
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return markup


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=menu_reply_keyboard(),
    )


@dp.message(F.text=="Tasks")
async def tasks_handler(message: Message):
    await message.answer("You requestet tasks list.")


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
