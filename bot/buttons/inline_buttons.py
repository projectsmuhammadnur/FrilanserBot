from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.buttons.text import phone, job, experiense, age, portfolio, save
from db.model import Merchants, Employers, Workers, Vacancies, Jobs


def worker_buttons():
    design = [
        [InlineKeyboardButton(text=phone, callback_data=phone), InlineKeyboardButton(text=job, callback_data=job)],
        [InlineKeyboardButton(text=experiense, callback_data=experiense),
         InlineKeyboardButton(text=age, callback_data=age)],
        [InlineKeyboardButton(text=portfolio, callback_data=portfolio)],
        [InlineKeyboardButton(text=save, callback_data=save)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


def yes_or_no_buttons():
    design = [
        [InlineKeyboardButton(text="✅", callback_data="✅"), InlineKeyboardButton(text="❌", callback_data="❌")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


def all_admins():
    ikm = InlineKeyboardMarkup(row_width=2)
    design_regions = []
    merchants = Merchants().select()
    for i in merchants:
        design_regions.append(InlineKeyboardButton(text=i[3], callback_data=i[1]))
    ikm.add(*design_regions)
    return ikm


def all_employers_button():
    ikm = InlineKeyboardMarkup(row_width=2)
    design_regions = []
    merchants = Employers().select()
    for i in merchants:
        design_regions.append(InlineKeyboardButton(text=i[2], callback_data=i[1]))
    ikm.add(*design_regions)
    return ikm


def all_vacancies_button():
    ikm = InlineKeyboardMarkup(row_width=2)
    design_regions = []
    merchants = Vacancies().select()
    for i in merchants:
        design_regions.append(InlineKeyboardButton(text=i[3], callback_data=i[1]))
    ikm.add(*design_regions)
    return ikm


def all_workers_button():
    ikm = InlineKeyboardMarkup(row_width=2)
    design_regions = []
    merchants = Workers().select()
    for i in merchants:
        design_regions.append(InlineKeyboardButton(text=i[2], callback_data=i[1]))
    ikm.add(*design_regions)
    return ikm


def all_jobs_button():
    ikm = InlineKeyboardMarkup(row_width=2)
    design_regions = []
    jobs = Jobs().select()
    for i in jobs:
        design_regions.append(InlineKeyboardButton(text=i[1], callback_data=i[1]))
    ikm.add(*design_regions)
    return ikm


def save_yes_or_no_button(job: str, user_id: str):
    design = [
        [InlineKeyboardButton(text="✅", callback_data=f"✅_{job.title()}_{user_id}"),
         InlineKeyboardButton(text="❌", callback_data=f"❌_{job.title()}_{user_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


def save_vacancies_from_workers(user_id: str):
    design = [
        [InlineKeyboardButton(text="Qabul qilaman✅", callback_data=f"agree_{user_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)
