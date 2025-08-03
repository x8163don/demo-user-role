from result import Result, Ok, Err
from sqlalchemy.orm import Session

from src.adapter.data import RoleModel, RoleDataSubjectModel, RoleTableModel, to_domain_role
from src.domain.aggregates.role import Role


class MariaDBRoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, input: Role) -> Result[Role, str]:
        try:
            with self.db.begin():

                role_model = RoleModel(name=input.name)
                self.db.add(role_model)
                self.db.flush()

                role_data_subjects = []
                for data_subject in input.data_subjects:
                    role_data_subject = RoleDataSubjectModel(role_id=role_model.id, data_subject_id=data_subject.id)
                    role_data_subjects.append(role_data_subject)

                if len(role_data_subjects) > 0:
                    self.db.add_all(role_data_subjects)

                role_tables = []
                for table in input.tables:
                    role_table = RoleTableModel(role_id=role_model.id, table_id=table.id)
                    role_tables.append(role_table)
                if len(role_tables) > 0:
                    self.db.add_all(role_tables)

                new_role = to_domain_role(role_model=role_model, role_data_subjects=role_data_subjects,
                                          role_tables=role_tables)
            return Ok(new_role)
        except Exception as e:
            return Err(f"Create user failed: {str(e)}")

    def update(self, input: Role) -> Result[Role, str]:
        try:
            with self.db.begin():
                role_model = self.db.query(RoleModel).filter_by(id=input.id, is_deleted=False).first()
                if not role_model:
                    return Err("Role not found")

                role_model.name = input.name

                self.db.query(RoleDataSubjectModel).filter_by(role_id=role_model.id).delete()
                self.db.query(RoleTableModel).filter_by(role_id=role_model.id).delete()

                role_data_subjects = [
                    RoleDataSubjectModel(role_id=role_model.id, data_subject_id=ds.id)
                    for ds in input.data_subjects
                ]
                if role_data_subjects:
                    self.db.add_all(role_data_subjects)

                role_tables = [
                    RoleTableModel(role_id=role_model.id, table_id=table.id)
                    for table in input.tables
                ]
                if role_tables:
                    self.db.add_all(role_tables)

                updated_role = to_domain_role(
                    role_model=role_model,
                    role_data_subjects=role_data_subjects,
                    role_tables=role_tables
                )
            return Ok(updated_role)

        except Exception as e:
            return Err(f"Update role failed: {str(e)}")

    def delete(self, input: Role) -> Result[Role, str]:
        try:
            with self.db.begin():
                role_model = self.db.query(RoleModel).filter_by(id=input.id, is_deleted=False).first()
                if not role_model:
                    return Err("Role not found")

                role_model.is_deleted = True

            return Ok(input)

        except Exception as e:
            return Err(f"Delete role failed: {str(e)}")

    def find_by_id(self, id: int) -> Result[Role, str]:
        try:
            role_model = self.db.query(RoleModel).filter_by(id=id, is_deleted=False).first()
            if not role_model:
                return Err("Role not found")

            role_data_subjects = self.db.query(RoleDataSubjectModel).filter_by(role_id=role_model.id).all()
            role_tables = self.db.query(RoleTableModel).filter_by(role_id=role_model.id).all()

            domain_role = to_domain_role(
                role_model=role_model,
                role_data_subjects=role_data_subjects,
                role_tables=role_tables
            )

            return Ok(domain_role)

        except Exception as e:
            return Err(f"Find role failed: {str(e)}")
