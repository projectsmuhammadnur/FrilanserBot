from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import worker_buttons, all_jobs_button, save_yes_or_no_button
from bot.buttons.reply_button import back_button, phone_number, main_menu_button
from bot.buttons.text import workers, phone, job, experiense, age, portfolio, back, save
from bot.dispatcher import dp
from db.model import Workers, Merchants


@dp.message_handler(Text(workers))
async def workers_handler(msg: types.Message, state: FSMContext):
    await state.set_state("workers")
    await msg.answer(text="Sizning malumotlaringiz ish beruvchiga ko`rinadi❗️", reply_markup=back_button())
    await msg.answer(text="Malumotlaringizni to`ldiring⬇️", reply_markup=worker_buttons())


@dp.callback_query_handler(Text(job), state='workers')
async def job_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state("enter_job")
    await call.message.edit_text(text="Kasbingizni tanlang⬇️", reply_markup=all_jobs_button())


@dp.callback_query_handler(state="enter_job")
async def enter_job(call: types.CallbackQuery, state: FSMContext):
    all_workers = Workers().select()
    for i in all_workers:
        if i[1] == str(call.from_user.id):
            Workers().update(user_id=str(call.from_user.id), job=call.data)
            await call.message.edit_text(text="Kasbingiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                                         reply_markup=worker_buttons())
            await state.set_state("workers")
            return
    Workers().insert_into(user_id=str(call.from_user.id), username=f"@{call.from_user.username}",
                          full_name=call.from_user.full_name, job=call.data)
    await call.message.edit_text(text="Kasbingiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                                 reply_markup=worker_buttons())
    await state.set_state("workers")


@dp.callback_query_handler(Text(experiense), state="workers")
async def job_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state("enter_experiense")
    await call.message.delete()
    await call.message.answer(text="Tajribangiz qancha:", reply_markup=back_button())


@dp.message_handler(state="enter_experiense")
async def enter_job(msg: types.Message, state: FSMContext):
    all_workers = Workers().select()
    for i in all_workers:
        if i[1] == str(msg.from_user.id):
            Workers().update(user_id=str(msg.from_user.id), experience=msg.text)
            await msg.answer(text="Tajribangiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                             reply_markup=worker_buttons())
            await state.set_state("workers")
            return
    Workers().insert_into(user_id=str(msg.from_user.id), username=f"@{msg.from_user.username}",
                          full_name=msg.from_user.full_name, experience=msg.text)
    await msg.answer(text="Tajribangiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                     reply_markup=worker_buttons())
    await state.set_state("workers")


@dp.callback_query_handler(Text(age), state="workers")
async def job_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state("enter_age")
    await call.message.delete()
    await call.message.answer(text="Yoshingiz qancha:\n\nFaqat son ishlating❗️", reply_markup=back_button())


@dp.message_handler(state="enter_age")
async def enter_job(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        all_workers = Workers().select()
        for i in all_workers:
            if i[1] == str(msg.from_user.id):
                Workers().update(user_id=str(msg.from_user.id), age=msg.text)
                await msg.answer(text="Yoshingiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                                 reply_markup=worker_buttons())
                await state.set_state("workers")
                return
        Workers().insert_into(user_id=str(msg.from_user.id), username=f"@{msg.from_user.username}",
                              full_name=msg.from_user.full_name, age=msg.text)
        await msg.answer(text="Yoshingiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                         reply_markup=worker_buttons())
        await state.set_state("workers")
    else:
        await state.set_state("enter_age")
        await msg.delete()
        await msg.bot.delete_message(msg.chat.id, msg.message_id - 1)
        await msg.answer(text="Yoshingiz qancha:\n\nFaqat son ishlating❗️", reply_markup=back_button())


@dp.callback_query_handler(Text(portfolio), state="workers")
async def job_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state("enter_portfolio")
    await call.message.delete()
    await call.message.answer(text="Portfolioingiz uchun havola:️", reply_markup=back_button())


@dp.message_handler(state="enter_portfolio")
async def enter_job(msg: types.Message, state: FSMContext):
    all_workers = Workers().select()
    for i in all_workers:
        if i[1] == str(msg.from_user.id):
            Workers().update(user_id=str(msg.from_user.id), portfolio=msg.text)
            await msg.answer(text="Portfolioingiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                             reply_markup=worker_buttons())
            await state.set_state("workers")
            return
    Workers().insert_into(user_id=str(msg.from_user.id), username=f"@{msg.from_user.username}",
                          full_name=msg.from_user.full_name, portfolio=msg.text)
    await msg.answer(text="Portfolioingiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                     reply_markup=worker_buttons())
    await state.set_state("workers")


@dp.callback_query_handler(Text(phone), state="workers")
async def job_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state("enter_phone_number")
    await call.message.delete()
    await call.message.answer(text="Telefon raqamingizni button orqali jo`nating:️", reply_markup=phone_number())


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="enter_phone_number")
async def phone_number_handler(msg: types.Message, state: FSMContext):
    phone_number = msg.contact.phone_number
    all_workers = Workers().select()
    for i in all_workers:
        if i[1] == str(msg.from_user.id):
            Workers().update(user_id=str(msg.from_user.id), phone=phone_number)
            await msg.answer(text="Telefon raqamingiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                             reply_markup=worker_buttons())
            await state.set_state("workers")
            return
    Workers().insert_into(user_id=str(msg.from_user.id), username=f"@{msg.from_user.username}",
                          full_name=msg.from_user.full_name, phone=phone_number)
    await msg.answer(text="Telefon raqamingiz saqlandi✅\n\nYana malumotingizni o`zgartirmoxchi bo`lsangiz⬇️",
                     reply_markup=worker_buttons())
    await state.set_state("workers")


@dp.callback_query_handler(Text(save), state="workers")
async def save_workers_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.bot.delete_message(call.from_user.id, call.message.message_id - 1)
    all_workers = Workers().select()
    for i in all_workers:
        if i[1] == str(call.from_user.id):
            for j in i:
                if j is None:
                    await state.set_state("workers")
                    await call.message.answer(text="Hali barcha maummotlaringiz to`lig` emas❗️",
                                              reply_markup=worker_buttons())
                    return
            await call.message.answer(text="Saqlandi✅", reply_markup=main_menu_button())
            for j in Merchants().select():
                await call.bot.send_message(chat_id=int(j[1]),
                                            text=f"🆕Yangi ish qabul qiluvchi\n\n🆔User-ID: {i[1]}\n👤Usename: {i[2]}\n📨Ism-Familiya: {i[3]}\n📲Telefon-raqami: {i[4]}\n🗣Yo`nalishi: {i[5]}\n🏢Tajribasi: {i[6]}\n📈Yoshi: {i[7]}\n👝Portfolio: {i[8]}",
                                            reply_markup=save_yes_or_no_button(job='workers',
                                                                               user_id=str(call.from_user.id)),
                                            disable_web_page_preview=True)
            await state.finish()
            return
    await state.set_state("workers")
    await call.message.answer(text="Hali barcha malumotlaringiz to`lig` emas❗️",
                              reply_markup=worker_buttons())


@dp.callback_query_handler(lambda call: call.data.startswith("agree"))
async def not_save_handler(call: types.CallbackQuery):
    atribute, user_id = call.data.split("_")
    for i in Workers().select():
        if i[1] == str(call.from_user.id):
            worker = i
    await call.bot.send_message(chat_id=int(user_id),
                                text=f"Vacansiyangizni qabul qilmoxchi✅\n\n👤Username: {worker[2]}\n📨Ism-Familiya: {worker[3]}\n📲Telefon: {worker[4]}\n🏢Tajriba: {worker[6]}\n👨🏻‍💻Yoshi: {worker[7]}\n👜Portfolio: {worker[8]}\n\nAgar rozi bo`lsangiz u bilan aloqaga chiqing✅")