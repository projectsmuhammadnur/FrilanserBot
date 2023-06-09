from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_button import main_menu_button, admin_menu, admins_menu, users_admin_button
from bot.buttons.text import back, statistic, admins
from bot.dispatcher import dp
from db.model import Users, Merchants


@dp.message_handler(commands='admin')
async def start_handler(msg: types.Message):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            await msg.answer(text=f"🏠{msg.from_user.first_name} admin menudasiz\n\nBo`limlardan birini tanlang⬇️", reply_markup=admin_menu())


@dp.message_handler(Text(statistic))
async def statistic_handler(msg: types.Message):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            users = Users().select()
            u = 0
            for i in users: u += 1
            await msg.answer(text=f"👥Userlar: {u}", reply_markup=users_admin_button())


@dp.message_handler(Text(admins))
async def admins_handler(msg: types.Message):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            merchant = Merchants().select()
            a = 0
            for i in merchant: a += 1
            await msg.answer(text=f"👤Adminlar: {a}\n\nBo`limlardan birini tanlang⬇️", reply_markup=admins_menu())