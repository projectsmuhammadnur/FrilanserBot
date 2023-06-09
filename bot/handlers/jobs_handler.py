from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import all_jobs_button
from bot.buttons.reply_button import back_job, jobs_buttons
from bot.buttons.text import add_job, back_jobs, sub_job
from bot.dispatcher import dp
from db.model import Jobs, Merchants


@dp.message_handler(Text(back_jobs), state='*')
async def back_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="Bo`limlardan birini tanlang⬇️", reply_markup=jobs_buttons())
    await state.finish()


@dp.message_handler(Text(add_job))
async def add_job_handler(msg: types.Message, state: FSMContext):
    await msg.delete()
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            await state.set_state('job_name')
            await msg.answer(text="Yo`nalish nomini kiriting: ", reply_markup=back_job())


@dp.message_handler(state="job_name")
async def add_job_handler(msg: types.Message, state: FSMContext):
    job = Jobs().insert_into(name=msg.text)
    await msg.answer(text="Yo`nlish saqlandi✅", reply_markup=jobs_buttons())
    await state.finish()


@dp.message_handler(Text(sub_job))
async def sub_job_handler(msg: types.Message, state: FSMContext):
    merchant = Merchants().select()
    for i in merchant:
        if i[1] == str(msg.from_user.id):
            await state.set_state("delete_jobs")
            await msg.answer(text="Diqqat❗️Siz yo`nlishlarni o`chirib yuborasiz",
                             reply_markup=back_job())
            await msg.answer(text="Qaysi yo`nlishni o`chirib yuborasiz⬇️", reply_markup=all_jobs_button())


@dp.callback_query_handler(state='delete_jobs')
async def delete_jobs_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    name = call.data
    Jobs().delete(name=name)
    await call.message.answer(text='Bu yo`nalish o`chirib tashlandi✅', reply_markup=jobs_buttons())
    await state.finish()