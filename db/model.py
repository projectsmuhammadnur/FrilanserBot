from db.config import DB


class Merchants(DB):
    def __init__(self, *fields):
        self.fields = fields


class Employers(DB):
    def __init__(self, *fields):
        self.fields = fields


class Jobs(DB):
    def __init__(self, *fields):
        self.fields = fields


class Workers(DB):
    def __init__(self, *fields):
        self.fields = fields


class Vacancies(DB):
    def __init__(self, *fields):
        self.fields = fields


class Users(DB):
    def __init__(self, *fields):
        self.fields = fields