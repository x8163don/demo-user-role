from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy.ext.declarative import declarative_base

from src.domain.aggregates.user import User
from src.domain.entities.user.role import Role

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "USER"

    id = Column("ID", MEDIUMINT(unsigned=True), primary_key=True, index=True)
    account = Column("ACCOUNT", String(64), unique=True, nullable=False)
    is_deleted = Column("IS_DELETE", Boolean, default=False)


class UserRoleModel(Base):
    __tablename__ = "USER_ROLE"

    user_id = Column("USER_ID", MEDIUMINT(unsigned=True), nullable=False, index=True)
    role_id = Column("ROLE_ID", MEDIUMINT(unsigned=True), nullable=False, index=True)


def to_domain_user(user_model: UserModel, user_roles: list[UserRoleModel]) -> User:
    result = User(id=user_model.id,
                  account=user_model.account)
    roles = []
    for user_role in user_roles:
        roles.append(Role(id=user_role.role_id))

    result.roles = roles

    return result
