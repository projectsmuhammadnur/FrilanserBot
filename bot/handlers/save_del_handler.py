from aiogram import types
from bot.dispatcher import dp
from db.model import Workers, Employers, Vacancies


@dp.callback_query_handler(lambda call: call.data.startswith("✅"))
async def save_handler(call: types.CallbackQuery):
    if call.data.split("_")[1] == "Vacancies":
        await call.bot.send_message(chat_id=-1001396522797, text=f"<b>{call.message.text}</b>", parse_mode="HTML")
    await call.message.edit_text(text="Saqlandi✅")


@dp.callback_query_handler(lambda call: call.data.startswith("❌"))
async def not_save_handler(call: types.CallbackQuery):
    atribute, job, id = call.data.split("_")
    if job == "Workers":
        Workers().delete(user_id=id)
    elif job == "Employers":
        Employers().delete(user_id=id)
    elif job == "Vacancies":
        Vacancies().delete(user_id=id)
    await call.message.edit_text(text="O`chirildi✅")