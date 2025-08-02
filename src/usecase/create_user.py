from result import Result, Err

from domain.aggregates.user import User
from src.usecase.interfaces.user_repository import UserRepository


class CreateUserUsecase:

    def __init__(self, repo_dict: dict[str, UserRepository]):
        self.repo_dict = repo_dict

    def execute(self, input: User, region: str = "HQ") -> Result[User, str]:
        repo = self.repo_dict[region]
        if repo is None:
            return Err("Region Not Found")

        result = repo.create(input)
        return result
