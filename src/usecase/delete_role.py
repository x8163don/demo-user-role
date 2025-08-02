from result import Ok, Err, Result

from domain.aggregates.role import Role
from usecase.interfaces.role_repository import RoleRepository


class DeleteRoleUsecase:

    def __init__(self, repo_dict: dict[str, RoleRepository]):
        self.repo_dict = repo_dict

    def execute(self, input: Role, region: str = "HQ") -> Result[Role, str]:
        repo = self.repo_dict[region]
        if repo is None:
            return Err("Region Not Found")

        result = repo.delete(input)
        if result.is_err():
            return Err(result.err())

        return Ok(result.ok_value)
