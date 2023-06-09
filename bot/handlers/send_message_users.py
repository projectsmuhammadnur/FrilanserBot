import types
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType, Message
from aiogram.utils.exceptions import ChatNotFound

from bot.buttons.reply_button import admin_menu, admin_back_button
from bot.buttons.text import send_message
from bot.dispatcher import dp
from db.model import Users, Merchants


@dp.message_handler(Text(send_message))
async def send_to_users(msg: types.Message, state: FSMContext):
    merchants = Merchants().select()
    for i in merchants:
        if i[1] == str(msg.from_user.id):
            text = "Habaringizni yuboring: "
            await msg.answer(text, 'MarkdownV2', reply_markup=admin_back_button())
            await state.set_state('get_message_for_all')


@dp.message_handler(state='get_message_for_all', content_types=ContentType.ANY)
async def get_user_id_for_send_to_user(msg: Message, state: FSMContext):
    await state.finish()
    users = Users().select()
    succ = 0
    fail = 0
    text = "*Session Started:*"
    session = await msg.bot.send_message(msg.chat.id, text, 'MarkdownV2')
    for user in users:
        try:
            await msg.copy_to(user[1], msg.caption, caption_entities=msg.caption_entities, reply_markup=msg.reply_markup)
            await sleep(0.05)
            succ += 1
        except ChatNotFound:
            pass
            try:
                pass
            except Exception:
                pass
            fail += 1
        except Exception:
            pass
            fail += 1
    else:
        await session.delete()
        await msg.answer(f"Habar *{succ}*ta userga tarqatildi✅\n*{fail}*ta user botni bloklagan❌", 'MarkdownV2', reply_markup=admin_menu())
