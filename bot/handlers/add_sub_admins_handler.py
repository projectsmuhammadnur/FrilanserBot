from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import yes_or_no_buttons, all_admins
from bot.buttons.reply_button import admin_back_button, admin_menu
from bot.buttons.text import add_admins, sub_admins, admin_back
from bot.dispatcher import dp
from db.model import Merchants, Users


@dp.message_handler(Text(admin_back), state='*')
async def back_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text=f"{msg.from_user.first_name} admin menudasiz🏠", reply_markup=admin_menu())
    await state.finish()


@dp.message_handler(Text(add_admins))
async def add_admin_handler(msg: types.Message, state: FSMContext):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            await state.set_state("add_admin")
            await msg.answer(text="Qo`shmoxchi bo`lgan admin 🆔ID sini yuboring: ", reply_markup=admin_back_button())


@dp.message_handler(state='add_admin')
async def add_admin_state_handler(msg: types.Message, state: FSMContext):
    merchants = Merchants().select()
    for i in merchants:
        if i[1] == str(msg.text):
            await state.set_state("add_admin")
            await msg.answer(text="Bu foydalanuvchi adminlar ro`yhatida mavjud❌\n\nQo`shmoxchi bo`lgan admin 🆔ID sini yuboring: ", reply_markup=admin_back_button())
            return
    users = Users().select()
    for i in users:
        if i[1] == str(msg.text):
            async with state.proxy() as data:
                data['user_id'] = i[1]
                data['username'] = i[3]
                data['full_name'] = i[2]
            await state.set_state("add_admin_yes_or_no")
            await msg.answer(text=f"Siz admin qilmoxchi bo`lgan user infosi❗️\n\n🆔ID: {i[1]}\n👤Usename: {i[3]}\nIsm-Familiya: {i[2]}\n\nAdmin qilishga rozimisiz <b>✅/❌</b>", parse_mode="HTML", reply_markup=yes_or_no_buttons())
            return
    await state.set_state("add_admin")
    await msg.answer(
        text="Bu foydalanuvchi botga start bosmagan❌\n\nQo`shmoxchi bo`lgan admin 🆔ID sini yuboring: ",
        reply_markup=admin_back_button())


@dp.callback_query_handler(state="add_admin_yes_or_no")
async def add_admin_yes_or_no_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        pass
    if call.data == '✅':
        merchant = Merchants().insert_into(user_id=data['user_id'], full_name=data['full_name'], username=data['username'])
        await call.message.answer(text="Yangi admin qo`shildi✅", reply_markup=admin_menu())
        await state.finish()
    else:
        await state.finish()
        await call.message.answer(text="Bekor qilindi✅", reply_markup=admin_menu())


@dp.message_handler(Text(sub_admins))
async def sub_admins_handler(msg: types.Message, state: FSMContext):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            await state.set_state("sub_admins")
            await msg.answer(text="Diqqat❗️Siz bir tugma bilan adminni o`chirasiz etborli bo`ling✅", reply_markup=admin_back_button())
            await msg.answer(text="Qaysi adminni o`chirasiz🗑", reply_markup=all_admins())


@dp.callback_query_handler(state='sub_admins')
async def sub_admin_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    merchant = call.data
    merchants = Merchants().select()
    for i in merchants:
        if i[1] == merchant:
            if i[1] == str(call.from_user.id):
                await state.set_state("sub_admins")
                await call.message.answer(text='Siz o`zingizni o`chira olmyasiz❗️ Qaysi adminni o`chirasiz🗑', reply_markup=all_admins())
            else:
                user = Merchants().delete(user_id=merchant)
                await call.message.answer(text="Bu admin o`chirib tashlandi✅", reply_markup=admin_menu())
                await state.finish()