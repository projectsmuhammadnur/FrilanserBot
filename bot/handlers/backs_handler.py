from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import worker_buttons
from bot.buttons.reply_button import main_menu_button, vacancies_button
from bot.buttons.text import back
from bot.dispatcher import dp


@dp.message_handler(Text(back), state=['enter_job', 'enter_experiense', 'enter_age', 'enter_portfolio', 'enter_phone_number'])
async def back_handler(msg: types.Message, state: FSMContext):
    await state.set_state("workers")
    await msg.answer(text="Malumotlaringizni to`ldiring⬇️", reply_markup=worker_buttons())


@dp.message_handler(Text(back), state=["add_vacancie_job", "add_vacancie_name", "add_vacancie_info", "add_price", "yes_or_no_add_vacancie"])
async def back_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="Bo`limlardan birini tanlang⬇️", reply_markup=vacancies_button())
    await state.finish()


@dp.message_handler(Text(back), state='*')
async def back_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text=f"{msg.from_user.first_name} asosiy menudasiz🏠", reply_markup=main_menu_button())
    await state.finish()