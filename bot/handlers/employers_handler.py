from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import save_yes_or_no_button
from bot.buttons.reply_button import phone_number, main_menu_button, back_button
from bot.buttons.text import employers
from bot.dispatcher import dp
from db.model import Employers, Merchants


@dp.message_handler(Text(employers))
async def workers_handler(msg: types.Message, state: FSMContext):
    await state.set_state('employer_phone_number')
    await msg.answer(text="Telefon raqamingizni jo`nating⬇️", reply_markup=phone_number())


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="employer_phone_number")
async def phone_number_handler(msg: types.Message, state: FSMContext):
    await state.finish()
    phone_number = msg.contact.phone_number
    all_merchants = Merchants().select()
    for i in all_merchants:
        await msg.bot.send_message(chat_id=int(i[1]),
                                   text=f"🆕Yangi ish beruvchu\n\n🆔User-ID: {msg.from_user.id}\n👤Usename: {msg.from_user.username}\n📨Ism-Familiya: {msg.from_user.full_name}\n📲Telefon-raqami: {phone_number}",
                                   reply_markup=save_yes_or_no_button(job='employers',
                                                                      user_id=str(msg.from_user.id)),
                                   disable_web_page_preview=True)
    all_employers = Employers().select()
    for i in all_employers:
        if i[1] == str(msg.from_user.id):
            Employers().update(user_id=str(msg.from_user.id), phone=phone_number)
            await msg.answer(text="Malumotlaringiz saqlandi✅",
                             reply_markup=main_menu_button())
            return
    Employers().insert_into(user_id=str(msg.from_user.id), username=f"@{msg.from_user.username}",
                            full_name=msg.from_user.full_name, phone=phone_number)
    await msg.answer(text="Malumotlaringiz saqlandi✅",
                     reply_markup=main_menu_button())
