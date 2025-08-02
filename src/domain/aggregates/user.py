from src.domain.entities.user.role import Role


class User:
    def __init__(self, id, account, roles: list[Role]):
        self.id = id
        self.account = account
        self.roles = roles


    def update_role(self, roles: list[Role]):
        self.roles = roles
