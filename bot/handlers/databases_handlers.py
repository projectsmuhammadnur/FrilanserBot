from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import all_employers_button, all_vacancies_button, all_workers_button
from bot.buttons.reply_button import databases_menu, admin_back_button, jobs_buttons, back_databases
from bot.buttons.text import databases, database_text, back_databses
from bot.dispatcher import dp
from db.model import Merchants, Employers, Vacancies, Workers


@dp.message_handler(Text(databases))
async def databases_handler(msg: types.Message):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            await msg.answer(text="Qaysi malumotlar bilan ishlamoxchisiz⬇️", reply_markup=databases_menu())


@dp.message_handler(Text(back_databses), state='*')
async def back_handler(msg: types.Message, state: FSMContext):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            await msg.answer(text="Qaysi malumotlar bilan ishlamoxchisiz⬇️", reply_markup=databases_menu())
            await state.finish()


@dp.message_handler(Text(database_text))
async def database_handler(msg: types.Message, state: FSMContext):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            if msg.text == "employers":
                await state.set_state("delete_employers")
                await msg.answer(text="Diqqat❗️Siz ish beruvchilarni o`chirib yuborasiz", reply_markup=back_databases())
                await msg.answer(text="Qaysi ish beruvchini o`chirib yuborasiz⬇️", reply_markup=all_employers_button())
            elif msg.text == "jobs":
                await msg.answer(text="Bo`limlardan birini tanlang⬇️", reply_markup=jobs_buttons())
            elif msg.text == "vacancies":
                await state.set_state("delete_vacancies")
                await msg.answer(text="Diqqat❗️Siz vakansiyalarni o`chirib yuborasiz",
                                 reply_markup=back_databases())
                await msg.answer(text="Qaysi vakansiyani o`chirib yuborasiz⬇️", reply_markup=all_vacancies_button())
            elif msg.text == "workers":
                await state.set_state("delete_workers")
                await msg.answer(text="Diqqat❗️Siz ish oluvchilarni o`chirib yuborasiz",
                                 reply_markup=back_databases())
                await msg.answer(text="Qaysi vakansiyani o`chirib yuborasiz⬇️", reply_markup=all_workers_button())


@dp.callback_query_handler(state='delete_employers')
async def delete_employers_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    employer = call.data
    employers = Employers().select()
    for i in employers:
        if i[1] == employer:
            user = Employers().delete(user_id=employer)
            await call.message.answer(text="Bu ish beruvchi o`chirib tashlandi✅", reply_markup=databases_menu())
            await state.finish()


@dp.callback_query_handler(state='delete_vacancies')
async def delete_vacancies_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    vacancie = call.data
    vacancies = Vacancies().select()
    for i in vacancies:
        if i[1] == vacancie:
            user = Vacancies().delete(user_id=vacancie)
            await call.message.answer(text="Bu ish beruvchi o`chirib tashlandi✅", reply_markup=databases_menu())
            await state.finish()


@dp.callback_query_handler(state='delete_workers')
async def delete_workers_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    worker = call.data
    workers = Workers().select()
    for i in workers:
        if i[1] == worker:
            user = Workers().delete(user_id=worker)
            await call.message.answer(text="Bu ish beruvchi o`chirib tashlandi✅", reply_markup=databases_menu())
            await state.finish()