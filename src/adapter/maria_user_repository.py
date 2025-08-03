from result import Result, Ok, Err
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.adapter.data import UserModel, UserRoleModel, to_domain_user
from src.domain.aggregates.user import User, Role


class MariaDBUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, input: User) -> Result[User, str]:
        try:
            with self.db.begin():

                user_model = UserModel(account=input.account)
                self.db.add(user_model)
                self.db.flush()

                user_roles = []
                for role in input.roles:
                    user_role = UserRoleModel(user_id=user_model.id, role_id=role.id)
                    user_roles.append(user_role)

                if len(user_roles) > 0:
                    self.db.add_all(user_roles)

            return Ok(User(user_model.id, user_model.account, input.roles))
        except Exception as e:
            return Err(f"Create user failed: {str(e)}")

    def update(self, user: User) -> Result[User, str]:
        try:
            with self.db.begin():
                user_model = self.db.query(UserModel).filter_by(id=user.id).first()
                if not user_model:
                    return Result.Err("User not found")

                user_model.account = user.account

                self.db.query(UserRoleModel).filter_by(user_id=user.id).delete()

                user_roles = []
                for role in input.roles:
                    user_role = UserRoleModel(user_id=user_model.id, role_id=role.id)
                    user_roles.append(user_role)

                if len(user_roles) > 0:
                    self.db.add_all(user_roles)

            return Ok(user)

        except Exception as e:
            return Err(f"Update user failed: {str(e)}")

    def delete(self, user: User) -> Result[User, str]:
        try:
            with self.db.begin():
                user_model = self.db.query(UserModel).filter_by(id=user.id, is_deleted=False).first()
                if not user_model:
                    return Result.Err("User not found")

                user_model.is_deleted = True

            return Ok(user)
        except Exception as e:
            return Err(f"Delete user failed: {str(e)}")

    def find_by_id(self, id: int) -> Result[User, str]:
        try:
            user_model = self.db.query(UserModel).filter_by(id=id).first()
            if not user_model:
                return Result.Err("User not found")

            user_roles = self.db.query(UserRoleModel).filter_by(user_id=id).all()

            user = to_domain_user(user_model=user_model, user_roles=user_roles)

            return Ok(user)
        except SQLAlchemyError as e:
            return Err(f"Find user failed: {str(e)}")
