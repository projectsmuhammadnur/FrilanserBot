from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import workers, employers, vakancies, back, statistic, databases, add_admins, admins, sub_admins, \
    admin_back, database_text, sub_job, add_job, back_databses, back_jobs, send_message, all_vacancies, add_vacancies
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_button():
    rkm = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rkm.add(workers, employers)
    rkm.add(vakancies)
    return rkm


def back_button():
    rkm = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rkm.add(back)
    return rkm


def admin_menu():
    rkm = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rkm.add(statistic, admins)
    rkm.add(databases)
    return rkm


def admins_menu():
    rkm = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rkm.add(add_admins, sub_admins)
    rkm.add(admin_back)
    return rkm


def admin_back_button():
    rkm = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rkm.add(admin_back)
    return rkm


def databases_menu():
    rkm = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for i in range(0, 3, 2):
        rkm.add(database_text[i], database_text[i+1])
    rkm.add(admin_back)
    return rkm


def jobs_buttons():
    rkm = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rkm.add(add_job, sub_job)
    rkm.add(back_databses)
    return rkm


def back_databases():
    rkm = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rkm.add(back_databses)
    return rkm


def back_job():
    rkm = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rkm.add(back_jobs)
    return rkm


def phone_handler():
    rmk = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rmk.add()


def users_admin_button():
    rmk = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rmk.add(send_message, admin_back)
    return rmk


def phone_number():
    design = [[KeyboardButton(text="Mening raqamim📲", request_contact=True)], [back]]
    markup = ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, one_time_keyboard=True)
    return markup

def vacancies_button():
    design = [
        [all_vacancies, add_vacancies],
        [back]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)