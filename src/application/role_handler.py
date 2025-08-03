from result import Result, Err

from src.application.input.create_role_input import CreateRoleInput
from src.application.input.delete_role_input import DeleteRoleInput
from src.application.input.update_role_permission_input import UpdateRolePermissionInput
from src.domain.aggregates.role import Role
from src.usecase.create_role import CreateRoleUsecase
from src.usecase.delete_role import DeleteRoleUsecase
from src.usecase.update_role_permission import UpdateRolePermissionUsecase


class RoleHandler:
    def __init__(self, create_role_uc: CreateRoleUsecase, delete_role_uc: DeleteRoleUsecase,
                 update_role_permission: UpdateRolePermissionUsecase):
        self.create_role_uc: CreateRoleUsecase = create_role_uc
        self.delete_role_uc: DeleteRoleUsecase = delete_role_uc
        self.update_role_permission: UpdateRolePermissionUsecase = update_role_permission

    def create_role(self, input: CreateRoleInput) -> Result[Role, str]:
        result = self.create_role.execute(input.to_domain())
        if result.is_ok():
            return result
        else:
            return Err(result.unwrap_err())

    def delete_role(self, input: DeleteRoleInput) -> Result[Role, str]:
        result = self.delete_role_uc.execute(input.to_domain())
        if result.is_ok():
            return result
        else:
            return Err(result.unwrap_err())

    def update_role_permission(self, input: UpdateRolePermissionInput) -> Result[Role, str]:
        result = self.update_role_permission.execute(input.to_domain())
        if result.is_ok():
            return result
        else:
            return Err(result.unwrap_err())
