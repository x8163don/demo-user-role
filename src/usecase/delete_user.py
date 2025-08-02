from result import Ok, Err, Result, is_ok, is_err
from domain.aggregates.user import User
from src.usecase.interfaces.user_repository import UserRepository


class DeleteUserUsecase:

    def __init__(self, repo_dict: dict[str, UserRepository]):
        self.repo_dict = repo_dict

    def execute(self, input: User, region: str = "HQ") -> Result[User, str]:
        repo = self.repo_dict[region]
        if repo is None:
            return Err("Region Not Found")

        result = repo.delete(input)
        if result.is_err():
            return Err(result.err())

        return Ok(input)
