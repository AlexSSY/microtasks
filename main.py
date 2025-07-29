import os
import sys
import logging
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Filter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import crud


dp = Dispatcher(storage=MemoryStorage())


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


class TaskIndexFilter(Filter):
    async def __call__(self, callback: CallbackQuery):
        if callback.data and callback.data.startswith("task:"):
            index = int(callback.data.split(":")[-1])
            return {"index": index}
        return False


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


async def get_navigation_keyboard(index: int, user_id: int):
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"task:{index-1}"))
    if index < await crud.user_tasks_count(user_id) - 1:
        buttons.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"task:{index+1}"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None


@dp.callback_query(TaskIndexFilter())
async def task_index_callback(callback: CallbackQuery, index: int):
    all_tasks = await crud.user_task_list(callback.from_user.id)
    task = all_tasks[index]
    keyboard = await get_navigation_keyboard(index, callback.from_user.id)
    await callback.message.edit_text(f"<b>{task.name}</b>", parse_mode="HTML", reply_markup=keyboard)
    await callback.answer()


@dp.message(F.text=="Tasks")
async def tasks_handler(message: Message):
    user = message.from_user
    if user is not None:
        tasks = await crud.user_task_list(user.id)
        if len(tasks) == 0:
            await message.answer("You have no tasks.")
        else:
            task = tasks[0]
            keyboard = await get_navigation_keyboard(0, message.from_user.id)
            await message.answer(f"<b>{task.name}</b>", parse_mode="HTML", reply_markup=keyboard)
    else:
        await message.answer("Sorry but this message must to be submitted by Telegram User.")


class AddTaskForm(StatesGroup):
    name = State()
    description = State()


@dp.message(F.text=="Add Task")
async def add_task_handler(message: Message, state: FSMContext):
    await message.answer("Enter task's name:")
    await state.set_state(AddTaskForm.name)


@dp.message(AddTaskForm.name)
async def add_task_name_handler(message: Message, state: FSMContext):
    name = message.text.strip()

    # validation
    if len(name) < 5:
        await message.answer("Name must be longer than 5 symbols.")
        return
    
    if len(name) > 25:
        await message.answer("Name must me shorter than 25 symbols.")
        return
    
    if await crud.first_task_by_name(name) is not None:
        await message.answer("Task with this name already exists.")
        return

    await state.update_data(name=name)
    await message.answer("Enter task's description:")
    await state.set_state(AddTaskForm.description)


@dp.message(AddTaskForm.description)
async def add_task_description_handler(message: Message, state: FSMContext):
    description = message.text.strip()

    # validation
    if len(description) < 5:
        await message.answer("Description must be longer than 5 symbols.")
        return
    
    if len(description) > 25:
        await message.answer("Description must me shorter than 25 symbols.")
        return
    
    data = await state.update_data(description=description)
    await crud.add_task(user_id=message.from_user.id, name=data.get("name"), description=data.get("description"))
    await message.answer(
        f"Task Created:\n\n"
        f"<b>Name:</b> {data['name']}\n"
        f"<b>Description:</b> {data['description']}",
        parse_mode=ParseMode.HTML
    )
    await state.clear()


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
