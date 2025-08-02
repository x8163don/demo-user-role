from result import Ok, Err, Result
from domain.aggregates.role import Role
from src.usecase.interfaces.role_repository import RoleRepository


class UpdateRolePermissionUsecase:

    def __init__(self, repo_dict: dict[str, RoleRepository]):
        self.repo_dict = repo_dict

    def execute(self, input: Role, region: str = "HQ") -> Result[Role, str]:
        repo = self.repo_dict[region]
        if repo is None:
            return Err("Region Not Found")

        current: Role

        result = repo.find_by_id(input.id)

        if result.is_err():
            return Err(result.err())
        current = result.ok_value

        current.update_permission(data_subjects=input.data_subjects, tables=input.tables)

        result = repo.update(current)
        if result.is_err():
            return Err(result.err())

        return Ok(current)
