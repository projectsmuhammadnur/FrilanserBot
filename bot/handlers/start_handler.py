from aiogram import types
from bot.buttons.reply_button import main_menu_button
from bot.dispatcher import dp
from db.model import Users, Merchants


@dp.message_handler(commands='start')
async def start_handler(msg: types.Message):
    await msg.answer(text=f"Assalomu aleykum {msg.from_user.first_name}👋\n\nBo`limlardan birini tanlang⬇️", reply_markup=main_menu_button())
    user = Users().select()
    for i in user:
        if i[1] == str(msg.from_user.id):
            return
    user = Users().insert_into(user_id=str(msg.from_user.id), full_name=msg.from_user.full_name,
                               username=f"@{msg.from_user.username}")
    merchant = Merchants().select()
    for i in merchant:
        await msg.bot.send_message(int(i[1]),text=f"👤Yangi user\n\n🆔ID: {msg.from_user.id}\n📝Ism-Familia: {msg.from_user.full_name}\n©️Username: @{msg.from_user.username}")