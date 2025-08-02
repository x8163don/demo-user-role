from src.domain.entities.role.data_subject import DataSubject
from src.domain.entities.role.table import Table


class Role:
    def __init__(self, id: int, name: str, data_subjects: list[DataSubject], tables: list[Table]):
        self.id = id
        self.name = name
        self.data_subjects = data_subjects
        self.tables = tables

    def update_permission(self,data_subjects: list[DataSubject], tables: list[Table]):
        self.data_subjects = data_subjects
        self.tables = tables