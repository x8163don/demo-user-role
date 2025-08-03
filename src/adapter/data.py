from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy.ext.declarative import declarative_base

from src.domain.aggregates.user import User
from src.domain.entities.role.data_subject import DataSubject
from src.domain.entities.role.table import Table
from src.domain.entities.user.role import Role
from src.domain.aggregates.role import Role as AggregateRole

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


class RoleModel(Base):
    __tablename__ = "ROLE"

    id = Column("ID", MEDIUMINT(unsigned=True), primary_key=True, index=True)
    name = Column("NAME", String(64), unique=True, nullable=False)


class RoleDataSubjectModel(Base):
    __tablename__ = "ROLE_DATA_SUBJECT"

    role_id = Column("ROLE_ID", MEDIUMINT(unsigned=True), primary_key=True, index=True)
    data_subject_id = Column("DATA_SUBJECT_ID", MEDIUMINT(unsigned=True), primary_key=True, index=True)


class RoleTableModel(Base):
    __tablename__ = "ROLE_TABLE"

    role_id = Column("ROLE_ID", MEDIUMINT(unsigned=True), primary_key=True, index=True)
    table_id = Column("TABLE_ID", MEDIUMINT(unsigned=True), primary_key=True, index=True)


def to_domain_role(role_model: RoleModel, role_data_subjects: list[RoleDataSubjectModel],
                   role_tables: list[RoleTableModel]) -> AggregateRole:
    result = AggregateRole(id=role_model.id, name=role_model.name)

    data_subjects = []
    for role_data_subject in role_data_subjects:
        data_subjects.append(DataSubject(id=role_data_subject.data_subject_id))
    result.data_subjects = data_subjects

    tables = []
    for role_table in role_tables:
        tables.append(Table(id=role_table.table_id))
    result.tables = tables

    return result
