from result import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.user_model import UserModel, user_role
from models.role_model import RoleModel
from src.domain.aggregates.user import User, Role

class MariaDBUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> Result[User, str]:
        try:
            user_model = UserModel(account=user.account)
            self.db.add(user_model)
            self.db.commit()
            self.db.refresh(user_model)

            # 建立 user.roles 的關聯
            for role in user.roles:
                role_model = self.db.query(RoleModel).filter_by(id=role.id).first()
                if role_model:
                    user_model.roles.append(role_model)

            self.db.commit()
            return Result.Ok(User(user_model.id, user_model.account, user.roles))
        except SQLAlchemyError as e:
            self.db.rollback()
            return Result.Err(f"Create user failed: {str(e)}")

    def update(self, user: User) -> Result[User, str]:
        try:
            user_model = self.db.query(UserModel).filter_by(id=user.id).first()
            if not user_model:
                return Result.Err("User not found")

            user_model.account = user.account

            # 更新角色
            user_model.roles.clear()
            for role in user.roles:
                role_model = self.db.query(RoleModel).filter_by(id=role.id).first()
                if role_model:
                    user_model.roles.append(role_model)

            self.db.commit()
            return Result.Ok(user)
        except SQLAlchemyError as e:
            self.db.rollback()
            return Result.Err(f"Update user failed: {str(e)}")

    def delete(self, user: User) -> Result[User, str]:
        try:
            user_model = self.db.query(UserModel).filter_by(id=user.id).first()
            if not user_model:
                return Result.Err("User not found")

            self.db.delete(user_model)
            self.db.commit()
            return Result.Ok(user)
        except SQLAlchemyError as e:
            self.db.rollback()
            return Result.Err(f"Delete user failed: {str(e)}")

    def find_by_id(self, id: int) -> Result[User, str]:
        try:
            user_model = self.db.query(UserModel).filter_by(id=id).first()
            if not user_model:
                return Result.Err("User not found")

            roles = [Role(role.id) for role in user_model.roles]
            user = User(user_model.id, user_model.account, roles)
            return Result.Ok(user)
        except SQLAlchemyError as e:
            return Result.Err(f"Find user failed: {str(e)}")
