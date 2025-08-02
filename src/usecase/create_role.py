from result import Result, Err

from domain.aggregates.role import Role
from usecase.interfaces.role_repository import RoleRepository


class CreateRoleUsecase:

    def __init__(self, repo_dict: dict[str, RoleRepository]):
        self.repo_dict = repo_dict

    def execute(self, input:Role, region: str = "HQ") -> Result[Role, str]:
        repo = self.repo_dict[region]
        if repo is None:
            return Err("Region Not Found")

        result = repo.create(input)
        return result
