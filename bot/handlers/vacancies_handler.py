from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import all_jobs_button, yes_or_no_buttons, save_yes_or_no_button, \
    save_vacancies_from_workers
from bot.buttons.reply_button import vacancies_button, back_button, main_menu_button
from bot.buttons.text import vakancies, all_vacancies, add_vacancies
from bot.dispatcher import dp
from db.model import Merchants, Workers, Employers, Vacancies


@dp.message_handler(Text(vakancies))
async def vacancies_main_menu_handler(msg: types.Message):
    await msg.answer(text="Bo`limlardan birini tanlang⬇️", reply_markup=vacancies_button())


@dp.message_handler(Text(all_vacancies))
async def all_vacancies_handler(msg: types.Message):
    await msg.answer(text="Barcha vacansiyalarni @ kanalidan olishingiz mumkin✅")


@dp.message_handler(Text(add_vacancies))
async def add_vacancies_handler(msg: types.Message, state: FSMContext):
    for i in Employers().select():
        if i[1] == str(msg.from_user.id):
            await state.set_state("add_vacancie_job")
            await msg.answer(text="Vakansiyangiz qaysi bo'limga tegishli: ", reply_markup=all_jobs_button())
            return
    await msg.answer(text="Siz hali ish beruvchi sifatida ro`yhatdan o`tmagansiz❗️", reply_markup=main_menu_button())


@dp.callback_query_handler(state="add_vacancie_job")
async def add_category_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["user_id"] = str(call.from_user.id)
        data['category'] = call.data
    await state.set_state("add_vacancie_name")
    await call.message.answer(text="Vacansiya nomini kiriting:", reply_markup=back_button())


@dp.message_handler(state="add_vacancie_name")
async def add_name_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['project_name'] = msg.text
    await state.set_state("add_vacancie_info")
    await msg.answer(
        text="Qo'shimcha malumot kiriting❗️\nMisol: Tushlik masalasi, O`zingizni shartlaringiz va boshqalar")


@dp.message_handler(state='add_vacancie_info')
async def add_info_handeler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = msg.text
    await state.set_state("add_price")
    await msg.answer(text="Maoshni kiriting:")


@dp.message_handler(state='add_price')
async def add_price_handeler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = msg.text
    await state.set_state("yes_or_no_add_vacancie")
    await msg.answer(
        text=f"Vakansiyangiz malumoti\nBo`lim: {data['category']}\nNomi: {data['project_name']}\nQo'shimcha: {data['info']}\nMaosh: {data['price']}\n\nShu vakansiya tarqalishiga rozimisiz❓",
        reply_markup=yes_or_no_buttons())


@dp.callback_query_handler(state="yes_or_no_add_vacancie")
async def yes_or_no_add_vacancie_handler(call: types.CallbackQuery, state: FSMContext):
    employer = tuple()
    async with state.proxy() as data:
        pass
    for i in Employers().select():
        if i[1] == str(call.from_user.id):
            employer = i
    if call.data == '✅':
        await call.message.delete()
        await call.message.answer(text="Barchaga jo`natildi✅", reply_markup=vacancies_button())
        for i in Merchants().select():
            await call.bot.send_message(int(i[1]),
                                        text=f"🆕Yangi vakansiya\n🆔ID: {employer[1]}\n👤Username: {employer[2]}\n📨Ism-Familiya: {employer[3]}\n📲Telefon-raqam: {employer[4]}\n📁Bo`lim: {data['category']}\n🏢Nomi: {data['project_name']}\n➕Qo'shimcha: {data['info']}\n💸Maosh: {data['price']}",
                                        reply_markup=save_yes_or_no_button(job='vacancies',
                                                                           user_id=str(call.from_user.id)))
        Vacancies().insert_into(user_id=data['user_id'], category=data['category'], project_name=data['project_name'],
                                info=data['info'], price=data['price'])
    for i in Workers().select():
        if i[5] == data['category']:
            await call.bot.send_message(int(i[1]),
                                        text=f"🆕Yangi vakansiya\n\n👤Username: {employer[2]}\n📲Telefon-raqam: {employer[4]}\n📁Bo`lim: {data['category']}\n🏢Nomi: {data['project_name']}\n➕Qo'shimcha: {data['info']}\n💸Maosh: {data['price']}",
                                        reply_markup=save_vacancies_from_workers(user_id=str(call.from_user.id)))
    await state.finish()
