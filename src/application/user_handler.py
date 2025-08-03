from result import Result, Err

from src.application.input.create_user_input import CreateUserInput
from src.application.input.delete_user_input import DeleteUserInput
from src.application.input.update_user_role_input import UpdateUserRoleInput
from src.domain.aggregates.user import User
from src.usecase.create_user import CreateUserUsecase
from src.usecase.delete_user import DeleteUserUsecase
from src.usecase.update_user_role import UpdateUserRoleUsecase


class UserHandler:
    def __init__(self, create_user_uc: CreateUserUsecase, delete_user_uc: DeleteUserUsecase,
                 update_user_uc: UpdateUserRoleUsecase):
        self.create_user_uc = create_user_uc
        self.delete_user_uc = delete_user_uc
        self.update_user_uc = update_user_uc

    def create_user(self, input: CreateUserInput) -> Result[User, str]:
        result = self.create_user_uc.execute(input.to_domain())
        if result.is_ok():
            return result
        else:
            return Err(result.unwrap_err())

    def delete_user(self, input: DeleteUserInput) -> Result[User, str]:
        result = self.delete_user_uc.execute(input.to_domain())
        if result.is_ok():
            return result
        else:
            return Err(result.unwrap_err())

    def update_user_role(self, input: UpdateUserRoleInput) -> Result[User, str]:
        result = self.update_user_uc.execute(input.to_domain())
        if result.is_ok():
            return result
        else:
            return Err(result.unwrap_err())
