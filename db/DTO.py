class UsersDto:
    def __init__(self,
                 id: int = None,
                 user_id: int = None,
                 full_name: str = None,
                 username: str = None,
                 created_at: str = None):
        self.id = id
        self.user_id = user_id
        self.full_name = full_name
        self.username = username
        self.created_at = created_at


class VacanciesDto:
    def __init__(self,
                 id: int = None,
                 user_id: int = None,
                 category: str = None,
                 project_name: str = None,
                 info : str = None,
                 price: int = None,
                 created_at: str = None):
        self.id = id
        self.user_id = user_id
        self.category = category
        self.project_name = project_name
        self.info = info
        self.price = price
        self.created_at = created_at